# Use the official python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

COPY ./app /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Exposure of the port
EXPOSE 5100

# Run the application
CMD ["python", "app.py"]
