#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
docker build --build-arg now="$(date +%Y-%m-%d_%H-%M-%S)" --tag "pytest-runner" ../../..
docker create --name dummy "pytest-runner"
docker cp dummy:app/src/term_assist/test/output/. output/
docker rm -f dummy
docker image rm -f pytest-runner
cd - || exit
