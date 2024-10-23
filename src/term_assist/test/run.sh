#!/usr/bin/env bash

# Navigate to the directory of the script
cd "$(dirname "$0")" || exit

# Build a Docker image with the tag "pytest-runner-image" from the Dockerfile
# at the project root
docker build --tag "pytest-runner-image" ../../..

# Get the current date and time in the format YYYY-MM-DD_HH-MM-SS
now=(date +%Y-%m-%d_%H-%M-%S)

# Run a Docker container with the name "pytest-runner-container" using the
# "pytest-runner-image". Pass environment variables from the .env file at the
# project root. Inside the container, create an output directory, run pytest on
# test.py, and save the output in both XML and log formats
docker run --name pytest-runner-container --env-file ../../../.env \
  pytest-runner-image /bin/bash -c \
  "mkdir output; python3 -m pytest test.py \
  --junit-xml=output/${now}_output.xml | tee output/${now}_output.log"

# Copy the output files from the container to the host machine's output
# directory
docker cp pytest-runner-container:app/src/term_assist/test/output/. output/

# Remove the Docker container
docker rm -f pytest-runner-container

# Remove the Docker image
docker image rm -f pytest-runner-image

# Return to the previous directory
cd - || exit
