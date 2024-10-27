package main

import (
    "os"
    "fmt"
    "time"
    "context"
    "os/signal"
    "net/http"
    "syscall"
    "github.com/sirupsen/logrus"
    logger "delivery-together-post-api/src/utils"
    "delivery-together-post-api/src/config"
    "delivery-together-post-api/src/infrastructure"
    postgres "delivery-together-post-api/src/infrastructure/database/postgres"
    // global "delivery-together-post-api/src/shared"
)

var log = logger.InitLogger()
var env config.Config = config.GetConfig()
var gormDB = postgres.GormDB{}

func InitServer(port string) {
    routers := infrastructure.CreateRouter()
    log.Info("Server activated")
    log.Info(fmt.Sprintf("The server is running 🟢 on port %s", env.PORT))
    if err := http.ListenAndServe(":"+port, routers); err != nil {
        log.Error("Something was wrong in the server: ", err)
        return
    }
}

func InitDataBase() {
    err := gormDB.Connect()
    if err != nil {
        log.WithFields(logrus.Fields{
            "error": err,
		}).Error("Error connecting with the database")

        return
    } else {
        // global.Database = gormDB.Context()
        log.Info("Database connected successfully")
    }
}
func CloseDatabase() {
    gormDB.Close()
}
func CloseServer(port string) {
    server := &http.Server{
        Addr: ":"+port,
    }

    // Create a context with a timeout for shutting down the server
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Error(fmt.Sprintf("Server shutdown error: %s\n", err))
    }
}

func InitSignal () {
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
    done := make(chan bool, 1)

    go func() {
        sig := <-sigChan
        log.Info(fmt.Sprintf("Received signal: %v", sig))
        CloseServer(env.PORT)
        CloseDatabase()
        os.Exit(0)
        done <- true
    }()
    log.Info("Application started. Press Ctrl+C to exit.")
    <-done

    log.Info("Application shutting down gracefully.")
}

func main() {
    InitDataBase()
    InitServer(env.PORT)
    InitSignal()
}