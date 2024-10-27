package config

import (
	"os"

	"github.com/joho/godotenv"
)

func GetConfig() Config {
	godotenv.Load()

	environment := os.Getenv("ENVIRONMENT")
	if environment == "" {
		environment = "develop"
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "3001"
	}

	config := Config{
		ENVIRONMENT: environment,
		PORT:        port,
		DB_USER:     os.Getenv("DB_USER"),
		DB_PASSWORD: os.Getenv("DB_PASSWORD"),
		DB_HOST:     os.Getenv("DB_HOST"),
		DB_PORT:     os.Getenv("DB_PORT"),
		DB_NAME:     os.Getenv("DB_NAME"),
		USERS_PATH:  os.Getenv("USERS_PATH"),
	}

	return config
}
