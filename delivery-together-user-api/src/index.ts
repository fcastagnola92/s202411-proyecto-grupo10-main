import app from './app';
import { config } from './config';
import { AppDataSource } from './config/data-source';

async function main() {
    try {
        await AppDataSource.initialize();
        app.listen(config.port, () => {
            console.log(`App is running on port: ${config.port}`);
        });
    } catch (error) {
        console.error(error)
    }

}

main()