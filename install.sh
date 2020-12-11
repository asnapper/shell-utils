#!/bin/bash
DOCKER_WRAPPER_IMAGE="$(docker build -q .)"

# yaml to json
echo "DOCKER_WRAPPER_IMAGE=$DOCKER_WRAPPER_IMAGE sh ./wrapper.sh python3 /scripts/yaml-to-json/" > ~/.bin/yaml-to-json
chmod +x ~/.bin/yaml-to-json

# json to yaml
echo "DOCKER_WRAPPER_IMAGE=$DOCKER_WRAPPER_IMAGE sh ./wrapper.sh python3 /scripts/json-to-yaml/" > ~/.bin/json-to-yaml
chmod +x ~/.bin/json-to-yaml