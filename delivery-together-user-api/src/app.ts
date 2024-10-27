import express from 'express';
import morgan from 'morgan';
import cors from 'cors';
import "reflect-metadata"
import userRoutes from './routes/user.routes'


const app = express();

app.use(morgan('dev'));
app.use(express.json());
app.use(cors());

app.use('/users', userRoutes);
export default app;