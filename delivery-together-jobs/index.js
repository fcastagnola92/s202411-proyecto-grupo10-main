import cron from 'node-cron';
import * as http from "http";
import 'dotenv/config';

cron.schedule(process.env.SCHEDULE, () => {
    console.log('running a task every minute');

    http.get(`${process.env.URL}/credit-cards/pending`, resp => {
        let data = "";
        resp.on("data", chunk => {
            console.log("Sending elements")
            data += chunk;
        });

        resp.on("end", () => {
            console.log(data);
        });
    }).on("error", err => {
        console.log("Error: " + err.message);
    });
});



