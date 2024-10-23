#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
docker build --tag "pytest-runner-image" ../../..
now=(date +%Y-%m-%d_%H-%M-%S)
docker run --name pytest-runner-container --env-file ../../../.env \
  pytest-runner-image /bin/bash -c \
  "mkdir output; python3 -m pytest test.py \
  --junit-xml=output/${now}_output.xml | tee output/${now}_output.log"
docker cp pytest-runner-container:app/src/term_assist/test/output/. output/
docker rm -f pytest-runner-container
docker image rm -f pytest-runner-image
cd - || exit
