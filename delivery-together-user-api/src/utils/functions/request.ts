import * as http from "http";

export function SendRequest(data: string, options: http.RequestOptions) {
    function onResponse(response: any) {
        let data = '';

        response.on('data', (chunk: object | string) => {
            data += chunk;
        });

        response.on('error', (error: Error) => {
            console.error('Error:', error.message);
        });

        response.on('end', () => {
            console.info('Response:', data);
        });
    }

    let request = http.request(options, onResponse);
    request.write(data);
    request.end();
}
