import { Status } from "../enums/status.enum"

export class RequestHookDTO {
    RUV: string
    userIdentifier: string
    createdAt: Date
    status: Status
    score: number
    verifyToken: string

}