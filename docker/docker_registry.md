docker search registry
docker pull registry
docker images
docker run -d -p 5000:5000 --name registry registry:latest
docker push ip:5000/registy/registry:latest
