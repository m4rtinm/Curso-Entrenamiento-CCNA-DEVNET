#!/bin/bash

TEMP_DIR=$(mktemp -d)
echo "Creando directorio temporal: $TEMP_DIR"

cp app.py Dockerfile $TEMP_DIR
echo "Archivos copiados al directorio temporal."

cd $TEMP_DIR

docker build -t webapp .
echo "Contenedor Docker construido con éxito."

docker run -d -p 7529:7529 webapp
echo "Contenedor Docker ejecutándose en el puerto 7529."

docker ps

curl http://localhost:7529
