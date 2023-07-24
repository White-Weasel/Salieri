# Install qdrant by docker on linux.
docker run -p 6333:6333 -d -v ~/qdrant:/qdrant/storage --name qdrant qdrant/qdrant && printf "\nQdrant started!"
