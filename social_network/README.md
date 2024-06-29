# Social Network Application


## Project Overview
This project is a social networking application built with Django Rest Framework. It provides functionalities such as user authentication, registration, login, friend requests, and user search . The application is containerized using Docker for easy deployment.


## Prerequisites
- Docker
- Docker Compose

## Installation

1. **Create and activate a virtual environment:**
    python3 -m venv env
    source env/bin/activate
    

2. **Install the dependencies:**
    pip install -r requirements.txt


## Management Commands

### Add Users

To add users using the Django management command:

python3 manage.py add_users

### Add Friendrequest

To add Friend request using the Django management command:

python3 manage.py add_friend_request
    
    
## Environment Setup

1. **Database Migrations:**
    python manage.py makemigrations
    python manage.py migrate

2. **Create a superuser:**
    python manage.py createsuperuser
    

3. **Run the development server:**
    python manage.py runserver
    

## Running the Application with Docker

1. **Build the Docker image:**
     docker-compose build

2. **Run the containers:**
    docker-compose up


## API Endpoints

- **User Registration:**
    - **Endpoint:** /api/register/
    - **Method:** "POST"
    - **Request Body:**
    json
      {
          "email": "user@example.com",
          "password": "optional_password"
      }
      

- **User Login:**
    - **Endpoint:** /api/login/
    - **Method:** "POST"
    - **Request Body:**
    json
      {
          "email": "user@example.com",
          "password": "password"
      }
    

- **Search Users:**
    - **Endpoint:** /api/search/
    - **Method:** "GET"
    - **Parameters:** email, name


- **Send Friend Request:**
    - **Endpoint:** /api/send_friend_request/
    - **Method:** "POST"
    - **Request Body:**
    json
      {
          "to_user": "recipient_user_id"
      }
    

- **Accept Friend Request:**
    - **Endpoint:** /api/accept_friend-request/
    - **Method:** "PUT"
    - **Request Body:**
    json
      {
        "request_id": "friend_request_id"
    }


**Reject Friend Request:**
    - **Endpoint:** /api/reject_friend_request/
    - **Method:** "PUT"
    - **Request Body:**
    json
      {
        "request_id": "friend_request_id"
    }

**List Accepted Friend Requests**

- **Endpoint:** /api/list_accepted_friend_request/
- **Method:** GET


**List Pending Friend Requests**

- **Endpoint:** /api/list_pending_friend_request/
- **Method:** GET