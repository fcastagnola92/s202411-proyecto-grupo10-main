package database

type Database interface {
    Connect() error
    Close() error
    Context() error
    Init() error
}