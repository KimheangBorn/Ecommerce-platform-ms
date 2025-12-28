const winston = require('winston');

const logger = winston.createLogger({
    level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    defaultMeta: { service: 'user-service' },
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.timestamp(),
                process.env.NODE_ENV === 'development'
                    ? winston.format.prettyPrint()
                    : winston.format.json()
            ),
        }),
    ],
});

module.exports = logger;
