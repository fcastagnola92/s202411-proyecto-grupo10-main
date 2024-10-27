package postgres


import	"fmt"
import "github.com/jinzhu/gorm"
import _ "github.com/jinzhu/gorm/dialects/postgres"
import "delivery-together-post-api/src/config"
import logger "delivery-together-post-api/src/utils"
import post "delivery-together-post-api/src/infrastructure/database/postgres/model"

var log = logger.InitLogger()

type GormDB struct {
    DB *gorm.DB
}

var env config.Config = config.GetConfig()
var gormDBInstance *GormDB 

func (g *GormDB) Close() error {
	return gormDBInstance.Close()
}

func (g *GormDB) Connect() error {
	db, err := gorm.Open("postgres", fmt.Sprintf("host=%s port=%s user=%s dbname=%s password=%s sslmode=disable",env.DB_HOST, env.DB_PORT, env.DB_USER, env.DB_NAME, env.DB_PASSWORD))
    if err != nil {
        return err
    }
    
      if err := db.AutoMigrate(&post.Post{}).Error; err != nil {
        log.Fatalf("Failed to auto-migrate table: %v", err)
    }

    
    gormDBInstance = &GormDB{DB: db}

    return nil
}

func Context() *GormDB {
    return gormDBInstance
}