package utils

import "testing"

func TestInitLogger(t *testing.T) {
    // Call the function to be tested
    logger := InitLogger()

    // Check if the logger instance is nil
    if logger == nil {
        t.Error("Expected non-nil logger instance, got nil")
    }
}