package httpClient

import model "delivery-together-post-api/src/infrastructure/httpClient/model"

type UserRepository interface {
	GetByToken(token string) (model.User, error)
}
