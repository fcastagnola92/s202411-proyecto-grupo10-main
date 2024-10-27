package post

import (
	postRepository "delivery-together-post-api/src/infrastructure/repositories/post"

	"github.com/sirupsen/logrus"
)

func ResetPost(repository postRepository.PostRepository) error {
	log.Info("Execution logic reset post")

	err := repository.Reset()

	if err != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": err,
		}).Error("Error trying to reset posts data")
		return err
	}

	return nil
}
