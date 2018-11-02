#!/usr/bin/env bash

if [ $# -ne 3 ]; then
  printf "Run the script like this: ./launch <mode> <environment> <version>... \nFor e.g. ./launch run dev 0.10.0"
  exit 1
fi

mode=$1
environment=$2
version=$3

git_repo="git@github.com:ankittyagi20/docker.git"
git_dir="/docker"

if [ $environment == "dev" ]; then
  image_name="flask:dev"
fi

if [ $environment == "qa" ]; then
  image_name="flask:qa"
fi

if [ $mode == "run" ]; then
  PORT="-p 9090:9090"
fi

docker build -t $image_name .
echo "PORT="$PORT
echo "IMAGE_NAME="$image_name

docker run -d $PORT -e "MODE=$mode" -e "ENVIRONMENT=$environment" -e "VERSION=$version" -e "REPO_URL=$git_repo" -e "REPO_DIR=$git_dir" $image_name
