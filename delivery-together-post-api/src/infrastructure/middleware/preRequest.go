package middleware

import (
    "net/http"
	"github.com/sirupsen/logrus"
	logger "delivery-together-post-api/src/utils"
)

func PreRequest(next http.Handler) http.Handler {
    // Define the middleware handler function
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log := logger.InitLogger()
		log.WithFields(logrus.Fields{
			"method": r.Method,
			"url": r.URL.Path,
		}).Info("Initialization request")

        // Call the next handler in the chain
        next.ServeHTTP(w, r)
    })
}