package post

import (
	model "delivery-together-post-api/src/infrastructure/database/postgres/model"
	adapter "delivery-together-post-api/src/infrastructure/outputs/posts/post/adapter"
	"errors"
	"fmt"
)

type PostMockRepository struct{}

var posts = []model.Post{}

func (m *PostMockRepository) Create(post model.Post) error {
	fmt.Println("Post repository mocked creation")

	if post.UserId == "2" {
		return errors.New("some error occurred")
	}

	posts = append(posts, post)

	return nil
}

func (m *PostMockRepository) Delete(id string) error {
	fmt.Println("Post repository mocked deleting")
	if id == "2" {
		return errors.New("some error occurred")
	}
	return nil
}

func (m *PostMockRepository) Filter(filters adapter.Filter) ([]model.Post, error) {
	fmt.Println("Post repository mocked filtering")

	for _, post := range posts {
		if post.UserId == "id-with-error" {
			return []model.Post{}, errors.New("some error occurred")
		}
	}

	return posts, nil
}

func (m *PostMockRepository) GetById(id string) (model.Post, error) {
	fmt.Println("Post repository mocked get by id")

	postResult := model.Post{}

	for _, post := range posts {
		if post.Id == id {
			postResult = post
		}
		if post.UserId == id {
			postResult = post
			return postResult, nil
		}
		if post.UserId == "id-with-error" {
			return postResult, errors.New("error getting the post")
		}
	}

	return postResult, nil
}

func (m *PostMockRepository) Get() ([]model.Post, error) {
	fmt.Println("Post repository mocked getting")
	for _, post := range posts {
		if post.UserId == "id-with-error" {
			return []model.Post{}, errors.New("some error occurred")
		}
	}
	return posts, nil
}

func (m *PostMockRepository) Reset() error {
	fmt.Println("Post repository mocked reset")

	for _, post := range posts {
		if post.UserId == "reset-error" {
			return errors.New("some error occurred")
		}
	}

	posts = []model.Post{}
	return nil
}
