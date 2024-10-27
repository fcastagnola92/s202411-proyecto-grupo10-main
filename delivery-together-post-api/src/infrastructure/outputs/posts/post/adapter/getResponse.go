package adapter

type GetResponse struct {
	Id string `json:"id"`
	RouteId string `json:"routeId"`
	UserId string `json:"userId"`
	ExpireAt string `json:"expireAt"`
	CreatedAt string `json:"createdAt"`
}