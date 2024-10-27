package post

import (
	"github.com/sirupsen/logrus"
	// import "delivery-together-post-api/src/infrastructure/inputs/adapter"

	model "delivery-together-post-api/src/infrastructure/database/postgres/model"

	postRepository "delivery-together-post-api/src/infrastructure/repositories/post"
)

func GetPost(id string, repository postRepository.PostRepository) (model.Post, error) {
	var post model.Post
	log.WithFields(logrus.Fields{
		"postId": id,
	}).Info("Execution get a post logic")
	

	post, errOnGetById := repository.GetById(id)

	if errOnGetById != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": errOnGetById,
		}).Error("Error getting post by id")
		return post, errOnGetById
	}

	return post, nil
}
