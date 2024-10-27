export class CreateUserDto {

    username: string;
    password: string;
    dni?: string | undefined;
    email: string;
    fullName?: string | undefined;
    phoneNumber?: string | undefined;

}