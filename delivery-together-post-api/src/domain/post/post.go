package post

import "time"


type Post struct {
    Id string
    RouteId string
	UserId string
	ExpireAt time.Time
	CreatedAt time.Time
}