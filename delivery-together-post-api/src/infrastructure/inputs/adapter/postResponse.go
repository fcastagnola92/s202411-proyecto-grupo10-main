package adapter

import "time"

type PostResponse struct {
	Id string `json:"id"`
	UserId string `json:"userId"`
	CreatedAt time.Time `json:"createdAt"`
}