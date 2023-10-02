ARG BASE_IMAGE=python:3.11.4-buster
ARG START=${BASE_IMAGE}

### add aditional layer for running the app behind a proxy
FROM ${BASE_IMAGE} as base_with_proxy
#host.docker.internal is  docker-desktop/windows specific 
#--add-host=host.docker.internal:host-gateway - to the build command to make it linux compatible
ENV HTTP_PROXY='host.docker.internal:3128'
ENV HTTPS_PROXY='host.docker.internal:3128'
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}

### Create base layer with just tooling ###
FROM ${START} as base
# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH
# Set workspace and copy poetry project files
WORKDIR /DevOps-Course-Starter
COPY poetry.toml pyproject.toml ./
# Install poetry main dependencies
RUN poetry install --only main

### Create prod layer containing application to run ###
FROM base as production
# Copy app into image
COPY todo_app/__init__.py todo_app/app.py todo_app/flask_config.py ./todo_app/
COPY todo_app/templates ./todo_app/templates/
COPY todo_app/data ./todo_app/data/
# Expose gunicorn app port
EXPOSE 8000 
# Run gunicorn command
CMD poetry run gunicorn --bind 0.0.0.0 'todo_app.app:create_app()'

### Create dev layer with additional dev tools ###
FROM base as development
#full poetry install main + dev
RUN poetry install
# export flask app port
EXPOSE 5080
# Run flask comand
CMD poetry run flask run -h 0.0.0.0 -p 5000
