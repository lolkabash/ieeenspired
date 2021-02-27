import parse from "csv-parse";
import fs from "fs";
import { Chemical } from "../types/chemical";

const loadData = async (file: string) => {
    const parser = fs
        .createReadStream(file)
        .pipe(parse({
            columns: true
        }));

    const records: Chemical[] = [];
    for await (const c of parser)
    {
        records.push({
            id: c["Identification Number"],
            substance: c["Substances and Materials"],
            identifier: c["Substance Identifier"],
            scope: c["Scope<s>3</s>"],
            threshold: c["Threshold Limit / Criteria<s>4</s>"],
            exemptions: c["Exemptions"],
            reference: c["References<s>5</s>"]
        } as Chemical);
    }

    return records;
}

export async function parseData(): Promise<Chemical[]>
{
    const a = await loadData(`./sample.csv`);
    return a;
}
