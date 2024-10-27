package httpClient

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"

	model "delivery-together-post-api/src/infrastructure/httpClient/model"

	"delivery-together-post-api/src/config"
	logger "delivery-together-post-api/src/utils"
)

var log = logger.InitLogger()
var env config.Config = config.GetConfig()

type UserHttpRepository struct{}

func (u *UserHttpRepository) GetByToken(token string) (model.User, error) {
	client := &http.Client{}
	var user model.User

	request, err := http.NewRequest("GET", fmt.Sprintf("%s/users/me", env.USERS_PATH), nil)

	if err != nil {
		return user, err
	}

	request.Header.Set("Authorization", fmt.Sprintf("Bearer %s", token))

	response, err := client.Do(request)
	if err != nil {
		fmt.Println("Error:", err)
		return user, err
	}
	defer response.Body.Close()

	if response.StatusCode == http.StatusOK {
		if err := json.NewDecoder(response.Body).Decode(&user); err != nil {
			return user, err
		}
		return user, err
	} else {
		return user, errors.New("Something was wrong during the token validation")
	}

}
