import { Request, Response } from "express";
import { StatusCodes } from "http-status-codes";
import { User } from "../entities/User";
import { Encrypt } from "../utils/functions/encrypt";
import { internalServerError, notFoundError, preconditionFailed } from "../utils/functions/handle-errors";
import { v4 as uuidv4 } from 'uuid';
import { CreateUserDto } from "../utils/dtos/create-user.dto";
import { CreateTokenDto } from "../utils/dtos/create-token.dto";
import { UpdateUserDto } from "../utils/dtos/update-user.dto";
import { Status } from "../utils/enums/status.enum";
import { event } from "../utils/events/true-native.event";
import { RequestHookDTO } from "../utils/dtos/request-hook-dto";
import { sendMail } from "../utils/functions/mailer";

/**
 * 
 * @param _req 
 * @param _res 
 * @returns 
 */
export const ping = async (body: Request, _res: Response): Promise<Response> => {
    return _res.status(200).send("Pong");
};

/**
 * 
 * @param body 
 * @param res 
 * @returns 
 */
export const create = async (body: CreateUserDto, res: Response): Promise<Response> => {
    try {
        const { username, password, email, dni, fullName, phoneNumber } = body;

        const userExists: User | null = await User.findOne({
            where: [
                { username },
                { email },
            ]
        });

        if (userExists) {
            return preconditionFailed(res)
        }

        const { hash, salt } = await Encrypt.cryptPassword(password);
        const user: User | null = new User();
        user.username = username;
        user.password = hash;
        user.email = email;
        user.dni = dni ?? '';
        user.fullName = fullName ?? '';
        user.phoneNumber = phoneNumber ?? '';
        user.salt = salt;

        await User.save(user);
        event.emit('verify', user);

        return res.status(StatusCodes.CREATED).json({
            id: user.id,
            createdAt: user.createdAt
        })
    } catch (error) {
        return internalServerError(res)
    }
};

/**
 * 
 * @param body 
 * @param res 
 * @returns 
 */
export const token = async (body: CreateTokenDto, res: Response): Promise<Response> => {
    const { username, password } = body;

    try {
        const user: User | null = await User.findOneBy({ username });

        if (!user) {
            return notFoundError(res);
        }
        const isUserNotVerified = user.status === Status.NO_VERIFICADO || user.status === Status.POR_VERIFICAR;

        if (isUserNotVerified) {
            return res.status(StatusCodes.UNAUTHORIZED).json({
                msg: "El usuario no esta VERIFICADO"
            });
        }
        const passwordMatch: boolean = await Encrypt.comparePassword(password, user.password);

        if (!passwordMatch) {
            return notFoundError(res);
        }

        const token: string = uuidv4();
        const expirationTime: Date = new Date();
        expirationTime.setMinutes(expirationTime.getMinutes() + 30);
        const formattedDate: string = expirationTime.toISOString();

        user.token = token;
        user.expireAt = formattedDate;

        await user.save();
        return res.status(StatusCodes.OK).json({
            id: user.id,
            token,
            expireAt: formattedDate,
        });

    } catch (error) {
        return internalServerError(res)
    }
};
/**
 * 
 * @param body 
 * @param res 
 * @returns 
 */
export const get = async (body: any, res: Response): Promise<Response> => {
    const { id, username, email, fullName, dni, phoneNumber, status } = body.user;

    try {
        return res.status(StatusCodes.OK).json(
            {
                id,
                username,
                email,
                fullName,
                dni,
                phoneNumber,
                status
            }
        );

    } catch (error) {
        return internalServerError(res)
    }
};

/**
 * 
 * @param id 
 * @param body 
 * @param res 
 * @returns 
 */
export const update = async (id: string, body: UpdateUserDto, res: Response): Promise<Response> => {
    const { status, dni, fullName, phoneNumber } = body;
    console.log(body)

    try {
        const user: User | null = await User.findOneBy({ id });

        if (!user) {
            return notFoundError(res);
        }
        user!.status = status;
        user!.dni = dni;
        user!.fullName = fullName;
        user!.phoneNumber = phoneNumber;


        await user.save()
        return res.status(StatusCodes.OK).json({
            msg: "el usuario ha sido actualizado"
        });
    } catch (error) {
        return internalServerError(res)
    }
}

/**
 * 
 * @param body 
 * @param res 
 * @returns 
 */
export const hook = async (body: RequestHookDTO, res: Response): Promise<Response> => {
    const { RUV, userIdentifier, score, status } = body;
    try {
        const user: User | null = await User.findOneBy({ id: userIdentifier });
        user!.status = status;
        await user!.save()

        sendMail(RUV, status, user);
        return res.status(StatusCodes.OK).json()

    } catch (error) {
        return internalServerError(res)
    }
}

export const reset = async (res: Response) => {
    try {
        await User.clear()
        return res.status(StatusCodes.OK).json({
            msg: "Todos los datos fueron eliminados"
        });
    } catch (error) {
        return internalServerError(res)
    }

}