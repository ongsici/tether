<!-- Dockerisation -->
docker buildx build --platform linux/amd64 -t ghcr.io/atchyuni/db-app:latest .
docker push ghcr.io/atchyuni/db-app:latest