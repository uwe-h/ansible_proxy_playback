#!/usr/bin/env bash

read -p "ACCESS_KEY: " ACCESS_KEY
read -p "SECRET_KEY: " SECRET_KEY
read -p "REGION: " REGION
docker-compose run  -e ACCESS_KEY=$ACCESS_KEY -e SECRET_KEY=$SECRET_KEY -e REGION=$REGION ec2sim /bin/bash
