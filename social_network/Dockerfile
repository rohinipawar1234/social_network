# Dockerfile

# Dockerfile for setting up a Django application in a Docker container.

FROM python:3.10

# Set environment variable to ensure the Python output is sent straight to the terminal (not buffered)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /code

# Allows docker to cache installed dependencies between builds
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Mounts the application code to the image
EXPOSE 8000

# runs the production server
CMD ["python","manage.py","runserver", "0.0.0.0:8000"]