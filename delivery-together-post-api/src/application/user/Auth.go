package user

import (
	model "delivery-together-post-api/src/infrastructure/httpClient/model"
	userRepository "delivery-together-post-api/src/infrastructure/repositories/httpClient"

	"github.com/sirupsen/logrus"

	logger "delivery-together-post-api/src/utils"
)

var log = logger.InitLogger()

func TokenValidator(token string, repository userRepository.UserRepository) (model.User, error) {
	var user model.User
	log.WithFields(logrus.Fields{
		"token": token,
	}).Info("Execution token validator")

	user, err := repository.GetByToken(token)

	if err != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": err,
		}).Error("Error in token validation")
		return user, err
	}

	return user, nil
}
