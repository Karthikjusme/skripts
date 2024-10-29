#!/bin/bash

# Function to build, push, and deploy a Docker image
build_push_deploy() {
    set -e
    IMAGE_NAME="xx.dkr.ecr.ap-south-1.amazonaws.com/actions-runner"
    IMAGE_VERSION="v1"

    DOCKERFILE="Dockerfile"
    BUILD_CONTEXT="."

    # Build Docker image
    docker build -t "${IMAGE_NAME}:${IMAGE_VERSION}" -f "${DOCKERFILE}" "${BUILD_CONTEXT}"

    # Push Docker image
    docker push "${IMAGE_NAME}:${IMAGE_VERSION}"

    set +e
}

# Call the function
build_push_deploy