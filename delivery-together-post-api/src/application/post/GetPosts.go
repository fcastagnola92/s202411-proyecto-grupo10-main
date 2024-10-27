package post

import (
	"github.com/sirupsen/logrus"
	model "delivery-together-post-api/src/infrastructure/database/postgres/model"
	postRepository "delivery-together-post-api/src/infrastructure/repositories/post"
	adapter "delivery-together-post-api/src/infrastructure/outputs/posts/post/adapter"
)

type Filter struct {
	Expire bool
	Route  string
	Owner  string
	UserId string
}

func GetPosts(repository postRepository.PostRepository) ([]model.Post, error) {
	var posts []model.Post
	log.Info("Execution get posts logic")

	posts, repositoryError := repository.Get()

	if repositoryError != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": repositoryError,
		}).Error("Error getting post")
		return posts, repositoryError
	}

	return posts, nil
}

func GetPostsFilter(filters adapter.Filter, repository postRepository.PostRepository) ([]model.Post, error) {
	var posts []model.Post
	log.Info("Execution get posts with filters logic")

	posts, repositoryError := repository.Filter(filters)

	if repositoryError != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": repositoryError,
		}).Error("Error getting post")
		return posts, repositoryError
	}
	return posts, nil
}
