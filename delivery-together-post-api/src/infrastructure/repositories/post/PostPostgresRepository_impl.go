package post

import (
	"errors"
	"time"

	postgres "delivery-together-post-api/src/infrastructure/database/postgres"
	model "delivery-together-post-api/src/infrastructure/database/postgres/model"

	adapter "delivery-together-post-api/src/infrastructure/outputs/posts/post/adapter"

	logger "delivery-together-post-api/src/utils"
)

var log = logger.InitLogger()

type PostPostgresRepository struct{}

func (p *PostPostgresRepository) Create(post model.Post) error {

	db := postgres.Context().DB

	if db == nil {
		return errors.New("database connection is nil")
	}
	result := db.Create(&post)
	if result.Error != nil {
		return result.Error
	}

	return nil
}

func (p *PostPostgresRepository) Get() ([]model.Post, error) {
	db := postgres.Context().DB
	var posts []model.Post

	if db == nil {
		return posts, errors.New("database connection is nil")
	}

	if err := db.Find(&posts).Error; err != nil {
		return posts, errors.New("failed to retrieve records")
	}

	return posts, nil
}

func (p *PostPostgresRepository) GetById(id string) (model.Post, error) {

	db := postgres.Context().DB
	post := model.Post{}

	if db == nil {
		return post, errors.New("database connection is nil")
	}

	if err := db.First(&post, "id = ?", id).Error; err != nil {
		return post, err
	}

	return post, nil
}

func (p *PostPostgresRepository) Filter(filters adapter.Filter) ([]model.Post, error) {

	db := postgres.Context().DB
	posts := []model.Post{}

	if db == nil {
		return posts, errors.New("database connection is nil")
	}

	query := db
	currentDate := time.Now().Format(time.RFC3339)
	if filters.Expire == true {
		query = query.Where("expire_at < ?", currentDate)
	} else if filters.Expire == false {
		query = query.Where("expire_at > ?", currentDate)
	}

	if filters.Route != "" {
		query = query.Where("route_id = ?", filters.Route)
	}

	if len(filters.Owner) > 0 {
		query = query.Where("user_id = ?", filters.UserId)
	}

	if err := query.Find(&posts).Error; err != nil {
		return posts, err
	}

	return posts, nil
}

func (p *PostPostgresRepository) Delete(id string) error {
	db := postgres.Context().DB

	if db == nil {
		return errors.New("database connection is nil")
	}

	if err := db.First(&model.Post{}, "id = ?", id).Error; err != nil {
		return err
	}

	if err := db.Where("id = ?", id).Delete(&model.Post{}).Error; err != nil {
		return err
	}

	return nil
}

func (p *PostPostgresRepository) Reset() error {
	db := postgres.Context().DB

	if db == nil {
		return errors.New("database connection is nil")
	}

	if err := db.Delete(&model.Post{}).Error; err != nil {
		return err
	}

	return nil
}
