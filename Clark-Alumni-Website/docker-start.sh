#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Initialize environment
echo "Initializing data"
python manage.py initialize_groups

# Create admin user -- REMOVE THIS FOR PRODUCTION
echo "Create admin user"
python manage.py safe_createsuperuser admin@clarku.edu admin

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
