package model

import 	"time"


type Post struct {
    Id   string `gorm:"primaryKey"`
    RouteId string `gorm:"column:route_id"`
    UserId    string `gorm:"column:user_id"`
	ExpireAt time.Time `gorm:"column:expire_at"`
    CreatedAt time.Time `gorm:"default:CURRENT_TIMESTAMP"`
}