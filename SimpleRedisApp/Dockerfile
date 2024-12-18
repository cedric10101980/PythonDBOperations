# Use the official python image as the base image
FROM python:3.9-alpine

# Add Labels to docker image
LABEL org.opencontainers.image.title="Flask App with Redis"
LABEL org.opencontainers.image.description="A Python Flask application using Redis, containerized with Docker."
LABEL org.opencontainers.image.authors="cedric10101980@gmail.com"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/cedric10101980/PythonOperations/tree/main/SimpleRedisApp"

# Set the working directory in the container
WORKDIR /app

COPY zscaler.cer .

# Change permissions of the .cer file to be readable by all users
RUN chmod a+r zscaler.cer

# Convert the .cer file to .pem
COPY zscaler.cer /usr/local/share/ca-certificates/zscaler.crt

# Update the certificate authorities
RUN update-ca-certificates


# Copy all files from the src directory to the working directory in the container
COPY ./src /app

# Install any dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exposure of the port
EXPOSE 5100

# Run the application
CMD ["python", "app.py"]
