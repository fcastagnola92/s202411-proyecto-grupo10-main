package config

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestConfig(t *testing.T) {
	config := Config{
		ENVIRONMENT: "test",
		PORT:        "3000",
		DB_USER:     "user",
		DB_PASSWORD: "p@$$w0rd",
		DB_HOST:     "host",
		DB_PORT:     "5000",
		DB_NAME:     "database",
		USERS_PATH:  "url",
	}

	assert.Equal(t, config.ENVIRONMENT, "test")
	assert.Equal(t, config.PORT, "3000")
	assert.Equal(t, config.DB_USER, "user")
	assert.Equal(t, config.DB_PASSWORD, "p@$$w0rd")
	assert.Equal(t, config.DB_HOST, "host")
	assert.Equal(t, config.DB_PORT, "5000")
	assert.Equal(t, config.DB_NAME, "database")
	assert.Equal(t, config.USERS_PATH, "url")
}
