# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install Poetry
# RUN pip install --no-cache-dir poetry

# # Use Poetry to install dependencies
# RUN poetry config virtualenvs.create false \
#   && poetry install --no-interaction --no-ansi

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start uWSGI
CMD ["python", "server.py"]