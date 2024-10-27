package post

import (
	"github.com/sirupsen/logrus"
	// import "delivery-together-post-api/src/infrastructure/inputs/adapter"

	postRepository "delivery-together-post-api/src/infrastructure/repositories/post"
)

func DeletePost(id string, repository postRepository.PostRepository) error {
	log.WithFields(logrus.Fields{
		"postId": id,
	}).Info("Execution logic to delete a post")

	err := repository.Delete(id)

	if err != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": err,
		}).Error("Error trying to delete the element")
		return err
	}

	return nil
}
