package model

type User struct {
    Id string `json:"id"`
    Username string `json:"username"`
	Email string `json:"email"`
	FullName string  `json:"fullName"`
	Dni string `json:"dni"`
	PhoneNumber string `json:"phoneNumber"`
	status string `json:"status"`
}