import winston from 'winston';

const { createLogger, format, transports } = winston;

const { LOG_LEVEL, NODE_ENV } = process.env;

const logFormatter = format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSS' }),
  winston.format.json(),
);

const logger = createLogger({
  level: LOG_LEVEL || 'debug',
  format: logFormatter,
  transports: [new transports.Console()],
});

function getNamespace(filePath: string) {
  if (!filePath) {
    return 'Not file info provided';
  }
  const folders = filePath.split('/');
  return folders[folders.length - 1];
}

export const Logger = (dirPath?: string) => {
  if (dirPath) {
    const namespace = getNamespace(dirPath);
    const environment = NODE_ENV;
    return logger.child({ namespace, environment });
  }
  return logger;
};