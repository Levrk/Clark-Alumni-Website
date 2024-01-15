# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Setup aliases
COPY tools/aliases.sh /
RUN set -ex ;\
    echo ". /aliases.sh" >> ~/.bashrc ;

# Copy project
COPY . .