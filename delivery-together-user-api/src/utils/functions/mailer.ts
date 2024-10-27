import * as http from "http";
import { config } from "../../config";
import { Email } from "../types/email.type";
import { SendRequest } from "./request";

export function sendMail(...data: string[] | string[] | any[]) {
    const [, , user] = data;
    const ruv = data[0];
    const status = data[1];

    const requestBody: Email = {
        to: user.email,
        subject: "Actualizacion de estado",
        message: `
        Usuario: ${user!.username} ${user.fullName}
        Número telefónico: ${user.phoneNumber},
        con RUV ${ruv}
        Su estado fue actualizado a ${status}`
    };
    const requestBodyString = JSON.stringify(requestBody);

    const options: http.RequestOptions = {
        hostname: config.mailHost,
        port: config.mailPort,
        path: config.mailPath,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    };
    SendRequest(requestBodyString, options);
}
