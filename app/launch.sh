#!/usr/bin/env bash

if [ $# -ne 3 ]; then
  printf "Run the script like this: ./launch <mode> <environment> <version>... \nFor e.g. ./launch run dev 0.10.0"
  exit 1
fi

mode=$1
environmemnt=$2
version=$3
#image_name=$4

if [ mode == 'run' ]; then
  PORT='-p 9090:9090'
fi

docker run -d -p $PORT $image_name -e MODE=$mode -e ENVIRONMENT=$environment -e VERSION=$version
