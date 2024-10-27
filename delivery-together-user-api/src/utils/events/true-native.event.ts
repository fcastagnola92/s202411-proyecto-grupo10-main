import * as http from "http"
import { EventEmitter } from 'events';
import { v4 as uuidv4 } from 'uuid';
import { User } from "../../entities/User";
import { TrueNativeVerify } from "../types/true-native-verify.type";
import { SendRequest } from "../functions/request";
import { config } from "../../config";

const event: EventEmitter = new EventEmitter();
event.on('verify', (user: User) => {
    const { email, dni, fullName, phoneNumber } = user;
    const { trueNativeHost, trueNativePort, trueNativePath, trueNativeUserWebHook, secretToken } = config;

    const requestBody: TrueNativeVerify = {
        transactionIdentifier: uuidv4(),
        userIdentifier: user.id,
        userWebhook: trueNativeUserWebHook,
        user: {
            email,
            dni,
            fullName,
            phone: phoneNumber
        }
    };
    const requestBodyString = JSON.stringify(requestBody);

    const options: http.RequestOptions = {
        hostname: trueNativeHost,
        port: trueNativePort,
        path: trueNativePath,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${secretToken}`
        }
    };
    SendRequest(requestBodyString, options);
});

event.on('error', (error) => {
    console.error(error);
});

export { event };

