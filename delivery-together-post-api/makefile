run:
	go run main.go

docker-run:
	go run main.go -b 0.0.0.0

build:
	go build -o app .


install:
	 go get -u github.com/axw/gocov/gocov
	 go mod tidy

test:
	go test ./... -tags mock

test-coverage:
	go test -cover ./... -tags mock

test-coverage-out:
	make create-coverage-folder
	go test -covermode=atomic -tags mock -coverprofile=./coverage/coverage.out ./...

test-coverage-report-ci:
	make test-coverage-out
	gocov convert ./coverage/coverage.out > ./coverage/coverage.json
	sh ./coverage_assestment.sh

test-coverage-report:
	make test-coverage-out
	${GOPATH}/bin/gocov convert ./coverage/coverage.out > ./coverage/coverage.json
	sh coverage_assestment.sh

test-coverage-report-html:
	make test-coverage-out
	go tool cover -html=./coverage/coverage.out -o ./coverage/coverage.html

create-coverage-folder:
	if [ ! -d "coverage" ]; then \
		echo "Coverage  folder doesn't exist"; \
		mkdir coverage; \
		echo "Coverage folder was created"; \
	else \
		echo "Coverage folder exist"; \
	fi