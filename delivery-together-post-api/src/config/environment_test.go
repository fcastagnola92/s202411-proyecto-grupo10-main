package config

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestEnvironment(t *testing.T) {

	assert.Equal(t, GetConfig().ENVIRONMENT, "develop")
	assert.Equal(t, GetConfig().PORT, "3001")
	assert.Equal(t, GetConfig().DB_HOST, "")
}
