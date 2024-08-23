Django Project Setup Instructions
Overview

This document provides step-by-step instructions for setting up and running the Django project. Follow these instructions to get the project up and running on your local development environment.
Steps to Setup the Django Project
1. Clone the Repository

First, you need to clone the repository containing the Django project. Use the following command to clone the repository:

bash

git clone https://github.com/aromals-github/InterestApp.git

2. Create and Activate a Virtual Environment

A virtual environment isolates  project’s dependencies. Follow these steps to create and activate a virtual environment:

    Install virtualenv (if not already installed):

    bash

pip install virtualenv

Create a virtual environment:

bash

virtualenv venv

This will create a directory named venv containing the virtual environment.

Activate the virtual environment:

    On Windows:

    bash

venv\Scripts\activate

On macOS and Linux:

bash

        source venv/bin/activate

    After activation, your command line prompt will change to indicate that the virtual environment is active.

3. Install Required Dependencies

With the virtual environment activated, install the required dependencies for the project:

bash

pip install -r requirements.txt

This command installs all the packages listed in the requirements.txt file.
4. Apply Database Migrations

Django uses migrations to manage changes to the database schema. Apply the migrations with the following command:

bash

python manage.py migrate

5. Create a Superuser (Optional)

To access the Django admin interface, create a superuser account:

bash

python manage.py createsuperuser

Follow the prompts to enter the superuser’s username, email, and password.
6. Run the Django Development Server

Start the Django development server with:

bash

python manage.py runserver

The server will start and be accessible at http://127.0.0.1:8000/ by default.
