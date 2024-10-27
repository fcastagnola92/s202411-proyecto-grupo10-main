package httpClient

import (
	model "delivery-together-post-api/src/infrastructure/httpClient/model"
	"errors"
)

type UserMockRepository struct{}

func (u *UserMockRepository) GetByToken(token string) (model.User, error) {
	user := model.User{
		Id:          "1",
		Username:    "test",
		Email:       "user@test.com",
		FullName:    "test fake",
		Dni:         "123456789",
		PhoneNumber: "5555555",
	}

	if token == "error-token" {
		return model.User{}, errors.New("error in authentication")
	}

	return user, nil

}
