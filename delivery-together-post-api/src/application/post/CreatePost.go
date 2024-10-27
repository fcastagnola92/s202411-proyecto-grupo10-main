package post

import (
	"errors"
	"time"

	"github.com/google/uuid"
	"github.com/sirupsen/logrus"

	"delivery-together-post-api/src/infrastructure/inputs/adapter"
	logger "delivery-together-post-api/src/utils"

	model "delivery-together-post-api/src/infrastructure/database/postgres/model"

	postRepository "delivery-together-post-api/src/infrastructure/repositories/post"
)

var log = logger.InitLogger()

func CreatePost(requestPost interface{}, repository postRepository.PostRepository) (model.Post, error) {
	modelPost := model.Post{}
	log.Info("Execution create post logic")

	log.WithFields(logrus.Fields{
		"requestPost": requestPost,
	}).Info("post to create")

	postMap, ok := requestPost.(adapter.PostToCreate)
	if !ok {
		errorMessage := "Failed to convert to map[string]interface{}"
		log.Error(errorMessage)
		return modelPost, errors.New(errorMessage)
	}

	parsedTime, err := time.Parse(time.RFC3339, postMap.ExpireAt)

	if err != nil {
		log.Error("Error convert ISO String to time")
		return modelPost, err
	}
	id := uuid.New()
	post := model.Post{
		Id:       id.String(),
		RouteId:  postMap.RouteId,
		UserId:   postMap.UserId,
		ExpireAt: parsedTime,
	}

	log.WithFields(logrus.Fields{
		"post": post,
	}).Info("post to save")

	repositoryError := repository.Create(post)

	if repositoryError != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": repositoryError,
		}).Error("Error creating product")
		return modelPost, repositoryError
	}

	log.Info("User created successfully")
	postCreated, errOnGetById := repository.GetById(post.Id)

	if errOnGetById != nil {
		log.WithFields(logrus.Fields{
			"errorMessage": errOnGetById,
		}).Error("Error getting post by id")
		return modelPost, errOnGetById
	}

	return postCreated, nil
}
