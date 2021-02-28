import { Chemical } from "@prisma/client";
import axios from "axios";

const base = process.env.ELASTIC_SEARCH;

export enum ElasticIndex
{
    CHEMICALS = "chemicals"
}

interface ElasticResult
{
    score: Number;
    source: Chemical;
}

export class Api
{
    static async indexChemicals(chemicals: Chemical[]): Promise<void>
    {
        try
        {
            // serialise Chemical into bulk string
            const bulk = chemicals
                .map(c => ({ id: c.id, substance: c.substance }))
                .map(c => `{"index":{"_id":"${c.id}"}}\n${JSON.stringify(c)}\n`)
                .join("");
    
            await axios({
                method: "PUT",
                url: `${base}/${ElasticIndex.CHEMICALS}/_bulk`,
                headers: {
                    "Content-Type": "application/json"
                },
                data: bulk
            });
        }
        catch (error)
        {
            console.error(error);
        }

    }

    static async query(indexName: ElasticIndex, query: String): Promise<ElasticResult[]>
    {
        try
        {
            const results = (await axios({
                method: "GET",
                url: `${base}/${indexName}/_search`,
                data: {
                    "query": {
                        "match": {
                            "substance": query
                        }
                    }
                }
            })).data;

            return results.hits.hits.map((r: any) => ({
                score: r._score,
                source: r._source
            }) as ElasticResult);
        }
        catch (error)
        {
            console.error(error);
            return [];
        }

    }

    static async deleteAll(indexName: ElasticIndex): Promise<void>
    {
        try
        {
            const results = (await axios({
                method: "DELETE",
                url: `${base}/${indexName}`,
            })).data;
        }
        catch (error)
        {
            console.error(error);
        }
    }

}