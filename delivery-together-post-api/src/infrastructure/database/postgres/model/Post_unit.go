package model

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestPost(t *testing.T) {
	date := time.Now().UTC()
	post := Post{
		Id:        "1",
		RouteId:   "1",
		UserId:    "1",
		ExpireAt:  date,
		CreatedAt: date,
	}

	assert.Equal(t, post.Id, "1")
	assert.Equal(t, post.RouteId, "1")
	assert.Equal(t, post.UserId, "1")
	assert.Equal(t, post.ExpireAt, date)
	assert.Equal(t, post.CreatedAt, date)
}
