# DevOps Apprenticeship: Project Exercise
![Build and Test](https://github.com/HOA1YOK/DevOps-Course-Starter/actions/workflows/ci-pipeline.yml/badge.svg?branch=main)
## Azure Deployment
The production deployment can be found running at: [`TodoApp.azurewebsites.net`](https://module8.azurewebsites.net/)

## DockerHub production image
https://hub.docker.com/r/adrianapadronhernando/todo_app

## System Requirements
### Docker
This project can be run in a docker container. To do so, first make sure you have docker properly installed. https://docs.docker.com/get-docker/

## Prerequisites
### Trello 
This application calls and sends requests to a trello board, before executing it.

1) Sign in or create a [trello.com](https://trello.com) account
2) generate a personal `API Key` and `Token` for authentication. (_To generate them,  access [this link](https://trello.com/app-key) **after** signing in into trello_)

### ENV variables and secrets
You'll need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

#### You will have to modify the `.env.template` file to create a `.env` file which includes the following variables and populate them accordingly.

```bash 
#save your secrets in .env
TRELLO_API_KEY=<your-trello-API-key>
TRELLO_TOKEN=<your-trello-token>
# we will also add a variable for the trello board_id value so it can be modified to the user's will.
BOARD_ID=<trello-board-id> 
```
_The `.env` file will be ignored by git (see: [`.gitignore`](.gitignore))_

## Running the App with docker compose

In this project you can build and run a docker image for both `Production` (using gunicorn to run the server) and `Development` targets (using flask for the server and allowing for dynamic debugging of the app). As well as a `Testing` target, containing the tests and testing environment.

Make sure you are running the app from the repository root folder (where the dockerfile and .dockerignore are located)

### Production
To build amd run the production target, use the following command:
``` bash 
docker compose up production
```

### Development
To build and run the development target, use the following command:
``` bash
docker compose up development
```

### Testing
To build and run the testing target, use the following command:
``` bash
docker compose up testing
```

Unlike the `production` target, `develoment` and `testing` images do not contain source code, instead, the `./todo_app` directory from this repository will be mounted to the running container. This will allow for dynamic development and debugging of the app.

## Github Actions
The following Github actions are set to run in this repository:

1) Build and Test Pipeline
    
    ![Build and Test](https://github.com/HOA1YOK/DevOps-Course-Starter/actions/workflows/ci-pipeline.yml/badge.svg?branch=main)
    - Triggered with any Push and Pull Request
    - Builds the app and runs the tests

## Making a new deployment
There are 2 steps to manually updating the current Azure deployment:
1) Build and Push a new container to docker hub
``` bash
docker compose build production
docker tag todo_app:prod adrianapadronhernando/todo_app
docker login
docker push adrianapadronhernando/todo_app
```
2) Perform a POST request to the azure [webhook URL](https://portal.azure.com/#@devops.corndel.com/resource/subscriptions/d33b95c7-af3c-4247-9661-aa96d47fccc0/resourceGroups/Cohort27_AdrHer_ProjectExercise/providers/Microsoft.Web/sites/module8/vstscd) to update the container to use
``` bash
curl -dH -X POST "<webhook>"
```
`Hint: remember to escape backslashes '\' with a $ in your command. eg: curl -dH -X POST "https://\$<deployment_username>:<deployment_password>@<webapp_name>.scm "`


# Alternative Methods to run the Todo_App

## Running with the Poetry virtual environment

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```
### Installing dependencies
The project will use a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```
### Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App with Docker
In this project you can build and run a docker image for both Production (using gunicorn to run the server) and Development (using flask for the server and allowing for dynamic debugging of the app). Make sure you are running the app from the repository root folder (where the dockerfile and .dockerignore are located)

### Production
#### Building the image
Has the basic main dependencies for the project

*(Add `--build-arg="START=base_with_proxy"` to the command line to build behind a proxy)*
``` bash 
docker build [--build-arg="START=base_with_proxy"] --target production --tag todo_app:prod .
```
#### Running the container
For running the Production image, you will need to pass your populated ```.env``` file containing your secrets through the ```docker run``` command:

``` bash
docker run --env-file ./.env -p 5000:8000 todo_app:prod
```
The gunicorn application will Run in port ```8000``` inside the container, so we can use ```-p``` to expose <host_port>:<container_port> to forward the app into our host port 5000 

### Development
#### Building the image
Has the main project dependencies as well as the development & testing dependencies installed

*(Add `--build-arg="START=base_with_proxy"` to the command line to build behind a proxy)*
```bash
docker build [--build-arg="START=base_with_proxy"] --target development --tag todo_app:dev .
```
#### Running the container
To take advantage of flask's development server that allows for dynamic hot reloading of code changes, we will use ```--mount``` to mount the app files into the container. This way the developer can perform changes in the local files, whilst still running the server in the container.

Once again you will still need to pass your populated ```.env``` file containing your secrets through the ```docker run``` command:

```bash 
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source=<full/path/to/app/files/todo_app>,target=/DevOps-Course-Starter/todo_app todo_app:dev
```
The Fask server will run in port ```5000``` inside of the container.

## Running Tests
You can run the test modules by running:
``` bash
poetry run pytest .
# or 
poetry run pytest <path-to-specific-test-file>
```
