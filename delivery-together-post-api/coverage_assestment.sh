#!/bin/bash

# Get coverage percentage from coverage file
coverage=$(go tool cover -func=./coverage/coverage.out | grep total | awk '{print $3}' | sed 's/%//')

# Define the coverage threshold (e.g., 80%)
threshold=70

# Compare coverage percentage against threshold
if (( $(echo "$coverage < $threshold" | bc -l) )); then
    echo "Coverage below threshold: $coverage%"
    exit 1
else
    echo "Coverage is sufficient: $coverage%"
fi