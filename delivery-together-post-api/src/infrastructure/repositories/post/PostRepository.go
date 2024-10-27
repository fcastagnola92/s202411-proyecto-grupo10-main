package post

import (
	model "delivery-together-post-api/src/infrastructure/database/postgres/model"
	adapter "delivery-together-post-api/src/infrastructure/outputs/posts/post/adapter"
)

type PostRepository interface {
	Create(post model.Post) error
	GetById(id string) (model.Post, error)
	Get() ([]model.Post, error)
	Filter(filters adapter.Filter) ([]model.Post, error)
	Delete(id string) error
	Reset() error
}
