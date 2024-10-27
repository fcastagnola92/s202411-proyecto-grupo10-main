import { Status } from "../enums/status.enum";

export class UpdateUserDto {

    status: Status;
    dni: string;
    fullName: string;
    phoneNumber: string;

}