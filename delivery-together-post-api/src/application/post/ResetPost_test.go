package post

import (
	"delivery-together-post-api/src/infrastructure/inputs/adapter"
	"delivery-together-post-api/src/infrastructure/repositories/post"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestResetPost(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "1",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}
	CreatePost(postToCreate, postRepository)
	err := ResetPost(postRepository)

	assert.Nil(t, err)
}

func TestResetPostWithError(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "reset-error",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}
	postRepository.Reset()
	CreatePost(postToCreate, postRepository)
	err := ResetPost(postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, err.Error(), "some error occurred")
}
