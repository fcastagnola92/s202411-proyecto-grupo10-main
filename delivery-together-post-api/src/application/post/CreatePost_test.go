package post

import (
	adapter "delivery-together-post-api/src/infrastructure/inputs/adapter"
	"delivery-together-post-api/src/infrastructure/repositories/post"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCreatePost(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "1",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}

	result, err := CreatePost(postToCreate, postRepository)

	assert.Nil(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, result.UserId, postToCreate.UserId)
	assert.Equal(t, result.RouteId, postToCreate.RouteId)
}

func TestCreatePostWithError(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "2",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}

	result, err := CreatePost(postToCreate, postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, err.Error(), "some error occurred")
	assert.NotNil(t, result)
	assert.Equal(t, result.UserId, "")
	assert.Equal(t, result.RouteId, "")
}

func TestCreatePostGetIdWithError(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "id-with-error",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}

	result, err := CreatePost(postToCreate, postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, err.Error(), "error getting the post")
	assert.NotNil(t, result)
}
