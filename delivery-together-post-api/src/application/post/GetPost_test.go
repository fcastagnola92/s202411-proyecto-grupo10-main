package post

import (
	"delivery-together-post-api/src/infrastructure/inputs/adapter"
	"delivery-together-post-api/src/infrastructure/repositories/post"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetPost(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "get1",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}
	postRepository.Reset()
	CreatePost(postToCreate, postRepository)

	post, err := GetPost("get1", postRepository)

	assert.Nil(t, err)
	assert.NotNil(t, post)
	assert.Equal(t, post.UserId, postToCreate.UserId)
	assert.Equal(t, post.RouteId, postToCreate.RouteId)
}

func TestGetPostWithError(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "id-with-error",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}
	postRepository.Reset()
	CreatePost(postToCreate, postRepository)

	post, err := GetPost("1", postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, err.Error(), "error getting the post")
	assert.Equal(t, post.UserId, "")
	assert.Equal(t, post.RouteId, "")
}
