# data_crawler

This repo contains script, dockerfile and docker compose file. I have uploaded the image on docker cloud so you can access it with following command:
docker pull berkaydemirtas/data_crawler

Or you can just run the docker compose file which automaticly use the image in dockerhub. Command is as follows:
docker-compose -f docker-compose.yml up --detach

Fields of my schema:

- id
- title
- location
- date
- time
- image_link
- artists[] (List of artists)
- works_list[] (List of works)

