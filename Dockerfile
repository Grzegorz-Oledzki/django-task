# Use the official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /image_task

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Copy the application code
COPY . .