package post

import (
	"delivery-together-post-api/src/infrastructure/repositories/post"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDeletePost(t *testing.T) {
	postRepository := &post.PostMockRepository{}

	err := DeletePost("1", postRepository)

	assert.Nil(t, err)
}

func TestDeletePostWithError(t *testing.T) {
	postRepository := &post.PostMockRepository{}

	err := DeletePost("2", postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, err.Error(), "some error occurred")
}
