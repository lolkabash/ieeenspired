import parse from "csv-parse";
import fs from "fs";
import { Chemical } from "@prisma/client";

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
            scope: c["Scope"],
            threshold: c["Threshold Limit / Criteria"],
            exemptions: c["Exemptions"],
            reference: c["References"]
        } as Chemical);
    }

    return records;
}

export async function parseData(): Promise<Chemical[]>
{
    const a = await loadData(`./sample.csv`);
    return a;
}
