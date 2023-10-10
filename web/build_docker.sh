#!/bin/sh
app="docker.test"
docker build -t ${app} .
docker run -p 56789:80 -d \
  --name=${app} \
  -v $PWD:/app ${app}