#!/bin/bash

# USAGE deploy.sh <image_name> <image_version>
# Function to build, push, and deploy a Docker image
build_push_deploy() {
    set -e
    IMAGE_NAME=$1
    IMAGE_VERSION=$2
    FUNCTION="cloudfront_invalidation"
    DOCKERFILE="Dockerfile"
    BUILD_CONTEXT="."

    # Build Docker image
    docker build -t "${IMAGE_NAME}:${IMAGE_VERSION}" -f "${DOCKERFILE}" "${BUILD_CONTEXT}"

    # Push Docker image
    docker push "${IMAGE_NAME}:${IMAGE_VERSION}"

    # Deploy to AWS Lambda
    aws lambda update-function-code --function-name "${FUNCTION}" --image-uri "${IMAGE_NAME}:${IMAGE_VERSION}" --region ap-south-1
    # sleep 10
    # aws s3 cp deploy.sh s3://m-prod-devops-s3/lambda_test/deploy.sh
    set +e
}

# Call the function
build_push_deploy