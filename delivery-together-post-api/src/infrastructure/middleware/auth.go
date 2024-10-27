package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/sirupsen/logrus"

	auth "delivery-together-post-api/src/application/user"

	logger "delivery-together-post-api/src/utils"

	model "delivery-together-post-api/src/infrastructure/httpClient/model"

	repository "delivery-together-post-api/src/infrastructure/repositories/httpClient"
)

// import "delivery-together-post-api/src/application/user/auth"

var log = logger.InitLogger()

func ValidateAuthentication(next http.Handler) http.Handler {
	// Define the middleware handler function
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var user model.User
		authHeader := r.Header.Get("Authorization")

		if authHeader == "" {
			http.Error(w, "Forbidden", http.StatusForbidden)
			log.Error("Forbidden user")
			return
		}

		if !strings.HasPrefix(authHeader, "Bearer ") {
			http.Error(w, "Invalid Authorization header", http.StatusUnauthorized)
			return
		}

		token := strings.TrimPrefix(authHeader, "Bearer ")

		log.WithFields(logrus.Fields{
			"token": token,
		}).Info("Received token")

		userRepository := &repository.UserHttpRepository{}

		user, err := auth.TokenValidator(token, userRepository)

		if err != nil {
			http.Error(w, "Forbidden", http.StatusUnauthorized)
			log.WithFields(logrus.Fields{
				"errorMessage": err,
			}).Error("Unauthorized")
			return
		}

		if token == "good" || token != "" {
			ctx := context.WithValue(r.Context(), "userID", user.Id)
			log.Info("User authenticated successfully")

			// Call the next handler in the chain
			next.ServeHTTP(w, r.WithContext(ctx))
		}

	})
}
