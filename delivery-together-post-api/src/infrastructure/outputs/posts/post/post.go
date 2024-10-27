package post

import (
	postLogic "delivery-together-post-api/src/application/post"
	model "delivery-together-post-api/src/infrastructure/database/postgres/model"
	adapter "delivery-together-post-api/src/infrastructure/outputs/posts/post/adapter"
	repository "delivery-together-post-api/src/infrastructure/repositories/post"
	logger "delivery-together-post-api/src/utils"
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
	"github.com/sirupsen/logrus"
)

var log = logger.InitLogger()

func GetPosts(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	queryValues := r.URL.Query()
	if len(queryValues) > 0 {
		HandleRequestWithQueryParams(w, r, queryValues)
	} else {
		HandleRequestWithoutParams(w, r)
	}
}

func GetPost(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	vars := mux.Vars(r)
	id := vars["id"]

	if !IsValidUUID(id) {
		w.WriteHeader(http.StatusBadRequest)
		log.Error("The uuid was invalid")
		return
	}

	postRepository := &repository.PostPostgresRepository{}

	post, err := postLogic.GetPost(id, postRepository)

	if err != nil {
		if err == gorm.ErrRecordNotFound {
			log.Error("Record not exists")
			w.WriteHeader(http.StatusNotFound)
		} else {
			http.Error(w, "Error on business layer", http.StatusInternalServerError)
			log.Error("Error on business layer")
		}
		return
	}

	data := adapter.GetResponse{
		Id:        post.Id,
		UserId:    post.UserId,
		RouteId:   post.RouteId,
		ExpireAt:  post.ExpireAt.Format(time.RFC3339),
		CreatedAt: post.CreatedAt.Format(time.RFC3339),
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)

}

func IsValidUUID(uuidStr string) bool {
	_, err := uuid.Parse(uuidStr)
	return err == nil
}

func HandleRequestWithoutParams(w http.ResponseWriter, r *http.Request) {
	postRepository := &repository.PostPostgresRepository{}
	posts, err := postLogic.GetPosts(postRepository)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Error("Something was wrong trying to get the posts")
		return
	}

	log.WithFields(logrus.Fields{
		"quantity": len(posts),
	}).Info("The getting was successfully")

	postResponse := make([]adapter.GetResponse, len(posts))
	for i, p := range posts {
		postResponse[i] = mapResponse(p)
	}

	jsonData, err := json.Marshal(postResponse)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func HandleRequestWithQueryParams(w http.ResponseWriter, r *http.Request, queryValues map[string][]string) {
	valid := false
	var expire string
	var route string
	var owner string

	if values, ok := queryValues["expire"]; ok && len(values) > 0 {
		expire = queryValues["expire"][0]
	}

	if values, ok := queryValues["route"]; ok && len(values) > 0 {
		route = queryValues["route"][0]
	}

	if values, ok := queryValues["owner"]; ok && len(values) > 0 {
		owner = queryValues["owner"][0]
	}

	log.WithFields(logrus.Fields{
		"query": logrus.Fields{
			"expire": expire,
			"route":  route,
			"owner":  owner,
			"userId": r.Context().Value("userID").(string),
		},
	}).Info("Request valid")

	var filters adapter.Filter

	valid = ValidateExpire(&expire)

	if !valid {
		log.Error("Invalid expire param")
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	if expire == "true" || expire == "false" {
		expireParsed, err := strconv.ParseBool(expire)

		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			log.Error("Something was wrong convert string to boolean")
			return
		}
		filters.Expire = expireParsed
	}

	valid = ValidateRoute(&route)

	if !valid {
		log.Error("Invalid route param")
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	filters.Route = route

	valid = ValidateOwner(&owner)

	if !valid {
		log.Error("Invalid owner param")
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	filters.Owner = owner

	if owner == "me" {
		filters.UserId = r.Context().Value("userID").(string)
	} else {
		filters.UserId = owner
	}

	postRepository := &repository.PostPostgresRepository{}
	posts, err := postLogic.GetPostsFilter(filters, postRepository)

	log.WithFields(logrus.Fields{
		"quantity": len(posts),
	}).Info("The getting was successfully")

	postResponse := make([]adapter.GetResponse, len(posts))
	for i, p := range posts {
		postResponse[i] = mapResponse(p)
	}

	jsonData, err := json.Marshal(postResponse)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func ValidateExpire(expire *string) bool {
	if expire == nil {
		return true
	}

	return *expire == "" || *expire == "true" || *expire == "false"
}

func ValidateRoute(route *string) bool {
	if route == nil || *route == "" {
		return true
	}

	return len(*route) > 0
}

func ValidateOwner(owner *string) bool {
	if owner == nil || *owner == "" {
		return true
	}

	return *owner == "me" || len(*owner) > 0
}

func mapResponse(p model.Post) adapter.GetResponse {
	return adapter.GetResponse{
		Id:        p.Id,
		RouteId:   p.RouteId,
		UserId:    p.UserId,
		ExpireAt:  p.ExpireAt.Format(time.RFC3339),
		CreatedAt: p.CreatedAt.Format(time.RFC3339),
	}
}
