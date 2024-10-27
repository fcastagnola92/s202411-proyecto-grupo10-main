package user

import (
	"delivery-together-post-api/src/infrastructure/httpClient/model"
	repository "delivery-together-post-api/src/infrastructure/repositories/httpClient"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAuth(t *testing.T) {
	userRepository := &repository.UserMockRepository{}

	result, err := TokenValidator("fake-token", userRepository)

	assert.Nil(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, result.Id, "1")
	assert.Equal(t, result.Username, "test")
	assert.Equal(t, result.Email, "user@test.com")
	assert.Equal(t, result.FullName, "test fake")
	assert.Equal(t, result.Dni, "123456789")
	assert.Equal(t, result.PhoneNumber, "5555555")
}

func TestAuthWithError(t *testing.T) {
	userRepository := &repository.UserMockRepository{}

	result, err := TokenValidator("error-token", userRepository)

	assert.NotNil(t, err)
	assert.Equal(t, result, model.User{})
	assert.Equal(t, err.Error(), "error in authentication")
}
