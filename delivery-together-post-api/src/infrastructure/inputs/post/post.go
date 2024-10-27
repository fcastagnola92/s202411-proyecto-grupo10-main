package post

import (
	postLogic "delivery-together-post-api/src/application/post"
	adapter "delivery-together-post-api/src/infrastructure/inputs/adapter"
	repository "delivery-together-post-api/src/infrastructure/repositories/post"
	logger "delivery-together-post-api/src/utils"
	"encoding/json"
	"errors"
	"net/http"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/google/uuid"
	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
	"github.com/sirupsen/logrus"
)

type PostRequest struct {
	RouteID  string `json:"routeId" validate:"required"`
	ExpireAt string `json:"expireAt" validate:"required,iso8601UTC"`
}

type DeleteResponse struct {
	Message string `json:"msg"`
}

type MessageResponse struct {
	Message string `json:"msg"`
}

var log = logger.InitLogger()

func Post(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	validate := validator.New()
	validate.RegisterValidation("iso8601UTC", ValidateISO8601UTCDateTime)

	var req PostRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Failed to parse request body", http.StatusBadRequest)
		log.Error("Failed to parse request body")
		return
	}
	if err := validate.Struct(req); err != nil {
		errors := map[string]string{}
		for _, e := range err.(validator.ValidationErrors) {
			errors[e.Field()] = e.Tag()
		}
		if _, ok := errors["ExpireAt"]; ok {
			data := MessageResponse{
				Message: "La fecha expiración no es válida",
			}

			jsonData, err := json.Marshal(data)
			if err != nil {
				http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
				return
			}
			w.WriteHeader(http.StatusPreconditionFailed)
			w.Write(jsonData)
			return
		}
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(errors)
		return
	}

	postToCreate := adapter.PostToCreate{
		UserId:   r.Context().Value("userID").(string),
		RouteId:  req.RouteID,
		ExpireAt: req.ExpireAt,
	}

	log.WithFields(logrus.Fields{
		"request": postToCreate,
	}).Info("Request valid")

	postRepository := &repository.PostPostgresRepository{}

	postToCreated, err := postLogic.CreatePost(postToCreate, postRepository)

	if err != nil {
		http.Error(w, "Error on business layer", http.StatusInternalServerError)
		log.Error("Error on business layer")
		return
	}

	data := adapter.PostResponse{
		Id:        postToCreated.Id,
		UserId:    postToCreated.UserId,
		CreatedAt: postToCreated.CreatedAt,
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
	w.Write(jsonData)
}

func DeletePost(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	vars := mux.Vars(r)
	id := vars["id"]

	if !IsValidUUID(id) {
		w.WriteHeader(http.StatusBadRequest)
		log.Error("The uuid was invalid")
		return
	}

	postRepository := &repository.PostPostgresRepository{}

	err := postLogic.DeletePost(id, postRepository)

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

	data := DeleteResponse{
		Message: "la publicación fue eliminada",
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func ResetPost(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	postRepository := &repository.PostPostgresRepository{}
	
	err := postLogic.ResetPost(postRepository)

	data := DeleteResponse{
		Message: "Todos los datos fueron eliminados",
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func ValidateISO8601UTCDateTime(fl validator.FieldLevel) bool {
	value := fl.Field().String()

	layout := "2006-01-02T15:04:05Z"

	// Attempt to parse the input value into a time.Time object
	_, err := time.Parse(layout, value)

	currentDate := time.Now()

	// Attempt to parse the input value into a time.Time object
	timeForValidate, err := time.Parse(time.RFC3339, value)

	if !timeForValidate.After(currentDate) {
		err = errors.New("The expired at cannot be in the pass")
	}

	log.WithFields(logrus.Fields{
		"error": timeForValidate.After(currentDate),
	}).Error("Validation error")

	return err == nil
}

func IsValidUUID(uuidStr string) bool {
	_, err := uuid.Parse(uuidStr)
	return err == nil
}
