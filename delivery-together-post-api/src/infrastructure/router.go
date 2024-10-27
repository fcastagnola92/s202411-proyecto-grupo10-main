package infrastructure

import (
    "net/http"
    "github.com/gorilla/mux"
    "delivery-together-post-api/src/infrastructure/outputs/posts/ping"
    postOutputs "delivery-together-post-api/src/infrastructure/outputs/posts/post"
    "delivery-together-post-api/src/infrastructure/inputs/post"
    "delivery-together-post-api/src/infrastructure/middleware"
)

func CreateRouter() *mux.Router {
    router := mux.NewRouter()

    router.Use(middleware.PreRequest)

    router.HandleFunc("/posts/ping", ping.Ping).Methods("GET")
    router.HandleFunc("/posts/reset", post.ResetPost).Methods("POST")
    postHandlerWithAuth := middleware.ValidateAuthentication(http.HandlerFunc(post.Post))
    router.Handle("/posts", postHandlerWithAuth).Methods("POST")

    getPostsWithAuth := middleware.ValidateAuthentication(http.HandlerFunc(postOutputs.GetPosts)) 
    getPostWithAuth := middleware.ValidateAuthentication(http.HandlerFunc(postOutputs.GetPost)) 
    router.Handle("/posts", getPostsWithAuth).Queries("expire", "{true|false}", "route", "{routeId}", "owner", "{id|me}").Methods("GET")
    router.Handle("/posts", getPostsWithAuth).Methods("GET")
    router.Handle("/posts/{id}", getPostWithAuth).Methods("GET")
    deletePostWithAuth := middleware.ValidateAuthentication(http.HandlerFunc(post.DeletePost)) 
    router.Handle("/posts/{id}", deletePostWithAuth).Methods("DELETE")

    return router
}