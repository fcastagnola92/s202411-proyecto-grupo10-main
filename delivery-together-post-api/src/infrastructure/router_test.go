package infrastructure

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRoutes(t *testing.T) {
	router := CreateRouter()

	ts := httptest.NewServer(router)
	defer ts.Close()

	tests := []struct {
		name           string
		method         string
		path           string
		expectedStatus int
	}{
		{
			name:           "Ping endpoint",
			method:         "GET",
			path:           "/posts/ping",
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		req, err := http.NewRequest(tc.method, ts.URL+tc.path, nil)
		if err != nil {
			t.Fatalf("Failed to create request: %v", err)
		}

		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			t.Fatalf("Request failed: %v", err)
		}
		defer func() {
			if resp != nil && resp.Body != nil {
				resp.Body.Close()
			}
		}()

		if resp == nil {
			t.Fatalf("Response is nil")
		}

		assert.Equal(t, tc.expectedStatus, resp.StatusCode, "Test '%s': unexpected status code", tc.name)

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			t.Fatalf("Failed to read response body: %v", err)
		}

		assert.Contains(t, string(body), "pong", "Test '%s': response body does not contain 'pong'", tc.name)

	}
}
