package user

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUser(t *testing.T) {
	post := User{
		Id:          "1",
		Username:    "user-test",
		Email:       "user-test@mail.com",
		Dni:         "123456",
		PhoneNumber: "123456789",
		Status:      "Active",
	}

	assert.Equal(t, post.Id, "1")
	assert.Equal(t, post.Username, "user-test")
	assert.Equal(t, post.Email, "user-test@mail.com")
	assert.Equal(t, post.Dni, "123456")
	assert.Equal(t, post.PhoneNumber, "123456789")
	assert.Equal(t, post.Status, "Active")
}
