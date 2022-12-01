#!/bin/bash
docker stop $(docker ps -aq)
docker container rm $(docker container ls -aq)
cd pe-portfolio
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build