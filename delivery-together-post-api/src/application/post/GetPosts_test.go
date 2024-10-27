package post

import (
	"delivery-together-post-api/src/infrastructure/inputs/adapter"
	adapterFilter "delivery-together-post-api/src/infrastructure/outputs/posts/post/adapter"
	"delivery-together-post-api/src/infrastructure/repositories/post"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSetup(t *testing.T) {
	var postRepository = &post.PostMockRepository{}
	postRepository.Reset()
}

func TestGetPosts(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "1",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}
	CreatePost(postToCreate, postRepository)
	posts, err := GetPosts(postRepository)

	assert.Nil(t, err)
	assert.NotNil(t, posts)
	assert.Equal(t, len(posts), 1)
}

func TestGetPostsWithError(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "id-with-error",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	postRepository := &post.PostMockRepository{}
	CreatePost(postToCreate, postRepository)
	posts, err := GetPosts(postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, len(posts), 0)
	assert.Equal(t, err.Error(), "some error occurred")
}

func TestGetPostsFilter(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "1",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	filters := adapterFilter.Filter{}
	postRepository := &post.PostMockRepository{}
	postRepository.Reset()
	CreatePost(postToCreate, postRepository)
	posts, err := GetPostsFilter(filters, postRepository)

	assert.Nil(t, err)
	assert.NotNil(t, posts)
	assert.Equal(t, len(posts), 1)
}

func TestGetPostsFilterWithError(t *testing.T) {
	postToCreate := adapter.PostToCreate{
		UserId:   "id-with-error",
		RouteId:  "2",
		ExpireAt: "2024-04-10T00:00:00.000Z",
	}
	filters := adapterFilter.Filter{}
	postRepository := &post.PostMockRepository{}
	CreatePost(postToCreate, postRepository)
	posts, err := GetPostsFilter(filters, postRepository)

	assert.NotNil(t, err)
	assert.Equal(t, len(posts), 0)
	assert.Equal(t, err.Error(), "some error occurred")
}
