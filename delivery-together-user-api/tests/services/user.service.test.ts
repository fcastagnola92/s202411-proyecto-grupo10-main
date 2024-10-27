// ping.test.ts
import { StatusCodes } from "http-status-codes";
import { CreateUserDto } from "../../src/utils/dtos/create-user.dto";
import request from "supertest";
import app from "../../src/app";
import { AppDataSource } from "../../src/config/data-source";
import { Status } from "../../src/utils/enums/status.enum";



beforeAll(async () => {
    await AppDataSource.initialize();

});

const mockBody: CreateUserDto = {
    username: 'testuser',
    password: 'testpassword',
    email: 'test@example.com',
    dni: '12345678A',
    fullName: 'Test User',
    phoneNumber: "3214445455"
};

let token: string;
let id: string;

describe("Ping service", () => {
    it('should respond with "Pong"', async () => {
        // ARRANGE
        const successResponse = "Pong";
        // ACTION
        const resp = await request(app).get(`/users/ping`);

        // ASSERT
        expect(resp.status).toBe(StatusCodes.OK);
        expect(resp.text).toBe(successResponse);
    });
});

describe('User create', () => {


    it('should return 201 if create a new user', async () => {
        // ARRANGE

        // ACTION
        const response = await request(app).post('/users').send(mockBody);
        // ASSERT
        expect(response.status).toBe(StatusCodes.CREATED);
        expect(response.body).toHaveProperty('id');
        expect(response.body).toHaveProperty('createdAt');


    });

    it('should return 412 precondition failed if user already exists', async () => {
        // ARRANGE
        const body: CreateUserDto = {
            username: mockBody.username,
            password: mockBody.password,
            email: mockBody.email,
        }

        // ACTION
        const response = await request(app).post('/users').send(body);

        // ASSERT
        expect(response.status).toBe(StatusCodes.PRECONDITION_FAILED);
    });
});

describe('Auth service', () => {

    it('should generate a token for a valid user', async () => {
        // ARRANGE
        const mockBody = {
            username: 'testuser',
            password: 'testpassword',
        };

        // ACTION
        const response = await request(app).post('/users/auth').send(mockBody);

        // ASSERT
        expect(response.status).toBe(StatusCodes.OK);
        expect(response.body).toHaveProperty('id');
        expect(response.body).toHaveProperty('token');
        expect(response.body).toHaveProperty('expireAt');
        token = response.body.token;
    });

    it('should return 404 not found for an invalid user', async () => {
        // Arrange
        const mockBody = {
            username: 'nonexistentuser',
            password: 'invalidpassword',
        };
        // Action
        const response = await request(app).post('/users/auth').send(mockBody);

        // Assert
        expect(response.status).toBe(StatusCodes.NOT_FOUND);
    });

    it('should return 404 not found for a user with incorrect password', async () => {
        // Arrange
        const mockBody = {
            username: 'testuser',
            password: 'incorrectpassword',
        };

        // Action
        const response = await request(app).post('/users/auth').send(mockBody);

        // Assert
        expect(response.status).toBe(StatusCodes.NOT_FOUND);
    });

});

describe('User get', () => {
    it('should return with user details', async () => {
        // ARRANGE

        const mockUser = {
            username: 'testuser',
            email: 'test@example.com',
            dni: '12345678A',
            fullName: 'Test User',
            phoneNumber: "3214445455",
            status: Status.POR_VERIFICAR
        };

        // ACTION
        const response = await request(app).get('/users/me').set('Authorization', `Bearer ${token}`);

        const addMockuser = {
            ...mockUser,
            id: response.body.id
        }

        // ASSERT
        expect(response.status).toBe(StatusCodes.OK);
        expect(response.body).toEqual(addMockuser)
        expect(response.body).toHaveProperty('id');
        expect(response.body.id).toEqual(expect.any(String));
        id = response.body.id;
    });

    it('should return 403 if not has TOKEN  ', async () => {
        // ARRANGE

        const path = '/users/me'

        // ACTION
        const response = await request(app).get(path);

        //ASSERT
        expect(response.status).toBe(StatusCodes.FORBIDDEN);
        expect(response.body).toEqual({});
    });
});

describe('User update', () => {
    it('should return with user updates values', async () => {
        // ARRANGE

        const mockUpdateUser = {
            username: 'testuserUpdated',
            email: 'testUpdated@example.com',
            dni: '12345678A111',
            fullName: 'Test User updated',
            phoneNumber: "3214445455",
            status: Status.VERIFICADO
        };
        const successResponse: string = 'el usuario ha sido actualizado'
        const path: string = `/users/${id}`

        // ACTION
        const response = await request(app).patch(path).send(mockUpdateUser)


        // ASSERT
        expect(response.status).toBe(StatusCodes.OK);
        expect(response.body.msg).toBe(successResponse)
    });

    it('should return 400 if not has status  ', async () => {
        // ARRANGE
        const badMockUpdateUser = {
            username: 'testuserUpdated',
            email: 'testUpdated@example.com',
            dni: '12345678A111',
            fullName: 'Test User updated',
            phoneNumber: "3214445455",
        };
        const path: string = `/users/${id}`

        // ACTION
        const response = await request(app).patch(path).send(badMockUpdateUser)

        // ASSERT
        expect(response.status).toBe(StatusCodes.BAD_REQUEST);
        expect(response.body).toEqual("");
    });

    it('should return 404 if not exists  ', async () => {
        // ARRANGE
        const mockUpdateUser = {
            username: 'testuserUpdated',
            email: 'testUpdated@example.com',
            dni: '12345678A111',
            fullName: 'Test User updated',
            phoneNumber: "3214445455",
            status: Status.VERIFICADO
        };
        const path: string = `/users/45ab091b-3600-4154-982e-a91ded0796d0`

        // ACTION
        const response = await request(app).patch(path).send(mockUpdateUser)

        // ASSERT
        expect(response.status).toBe(StatusCodes.NOT_FOUND);
        expect(response.body).toEqual({});
    });
});

describe("User reset", () => {
    it('should return 200 if DB is reset', async () => {
        // ARRANGE
        const successResponse = 'Todos los datos fueron eliminados'
        // ACTION
        const resp = await request(app).post(`/users/reset`);
        console.log(resp)

        // ASSERT
        expect(resp.status).toBe(StatusCodes.OK);
        expect(resp.body.msg).toBe(successResponse)
    });
});
