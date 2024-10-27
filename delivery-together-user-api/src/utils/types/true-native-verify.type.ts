export type TrueNativeVerify = {
    transactionIdentifier: string;
    userIdentifier: string;
    userWebhook: string;
    user: {
        email: string;
        dni: string;
        fullName: string;
        phone: string;
    };
};