#!/bin/sh
app="docker.test"
docker build -t ${app} .
docker run -p 56890:8000 -d \
  --name=${app} \
  -v $PWD:/app ${app}