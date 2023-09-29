ARG BASE_IMAGE=python:3.11.4-buster
ARG START=${BASE_IMAGE}

#add aditional layer for running the app behind a proxy
FROM ${BASE_IMAGE} as base_with_proxy

#host.docker.internal is  docker-desktop/windows specific 
#--add-host=host.docker.internal:host-gateway - to the build command to make it linux compatible
ENV HTTP_PROXY='host.docker.internal:3128'
ENV HTTPS_PROXY='host.docker.internal:3128'
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}

# Create base layer with just tooling
FROM ${START} as base

# Install poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install poetry

# Set woekspace and copy poetry project files
WORKDIR /DevOps-Course-Starter
COPY poetry.toml pyproject.toml ./

# Install poetry dependencies
RUN poetry install

# Create prod layer containing application to run 
FROM base as prod

EXPOSE 5000

# Copy app into image
COPY todo_app ./todo_app/

# Run gunicorn command
CMD [ "poetry run gunicorn --bind 0.0.0.0 'todo_app.app:create_app()'" ]
