package utils

import "os"
import "github.com/sirupsen/logrus"
import "delivery-together-post-api/src/config"

func InitLogger() *logrus.Entry {
    config := config.GetConfig()
    logger := logrus.New()

    logger.SetLevel(logrus.DebugLevel)

    logger.SetOutput(os.Stdout)

    logger.SetFormatter(&logrus.JSONFormatter{})

    return logger.WithFields(logrus.Fields{
        "environment":  config.ENVIRONMENT,
    })
}