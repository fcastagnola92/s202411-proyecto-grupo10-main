import express, { Application } from "express";
import bodyParser from "body-parser";
import cors from "cors";
import router from "@Infrastructure/router";
import PreRequest from "@Infrastructure/middleware";

const app: Application = express();
app.use(bodyParser.json());
app.use(PreRequest);

app.use(router);

app.use(cors());

export default app;
