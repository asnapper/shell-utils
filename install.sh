#!/bin/bash
DOCKER_WRAPPER_IMAGE="$(docker build -q .)"

cp wrapper.sh ~/.bin/

# yaml to json
echo "DOCKER_WRAPPER_IMAGE=$DOCKER_WRAPPER_IMAGE sh ~/.bin/wrapper.sh python3 /scripts/yaml-to-json/" > ~/.bin/yaml-to-json
chmod +x ~/.bin/yaml-to-json

# json to yaml
echo "DOCKER_WRAPPER_IMAGE=$DOCKER_WRAPPER_IMAGE sh ~/.bin/wrapper.sh python3 /scripts/json-to-yaml/" > ~/.bin/json-to-yaml
chmod +x ~/.bin/json-to-yaml

# json to yaml
echo "DOCKER_WRAPPER_IMAGE=$DOCKER_WRAPPER_IMAGE sh ~/.bin/wrapper.sh python3 /scripts/mod-dep/ \$@" > ~/.bin/mod-dep
chmod +x ~/.bin/mod-dep