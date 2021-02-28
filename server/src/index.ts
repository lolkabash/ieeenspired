require("dotenv").config();
import express from "express";
const app = express();
const port = process.env.PORT;

import elastic from "./controller/elastic";

app.use(express.json());

app.get("/", (req, res) => {
    res.send("api healthy");
});

app.use("/search", elastic);

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`)
});