import { DataSource } from 'typeorm';
import { config } from '.';
import { User } from '../entities/User';

export const AppDataSource = new DataSource({
    type: "postgres",
    host: config.dbHost,
    port: 5432,
    username: config.dbUserName,
    password: config.dbPassword,
    database: config.dbName,
    synchronize: true,
    logging: true,
    entities: [User],
    subscribers: [],
    migrations: [],
})