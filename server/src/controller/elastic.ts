import express from "express";
import * as Elastic from "../api/elastic";
import { parseData } from "../api/parser";
const router = express.Router();

// query ?params
router.get("/", async (req, res) => {
    const { query } = req.query;

    if (!query || !(typeof query === "string")) return res.status(400).send();

    const searchResults = await Elastic.Api.query(Elastic.ElasticIndex.CHEMICALS, query);
    res.send(searchResults);
});

// rescrape and index results
router.post("/", async (req, res) => {
    // const chemicals: Chemical[] = [{
    //     id: "12345",
    //     substance: "testing 12345",
    // }];
    const chemicals = await parseData();
    await Elastic.Api.indexChemicals(chemicals);


    res.status(204).send();
});

export default router;