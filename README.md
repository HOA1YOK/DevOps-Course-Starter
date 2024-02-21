# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```
### Docker
This project can also be run in a docker container. To do so, first make sure you have docker properly installed. https://docs.docker.com/get-docker/

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

## Prerequisites

This application calls and sends requests to a trello board, before executing it you should have a [trello.com](https://trello.com) account and generate a personal API Key and Token for authentication.
 - To generate get your API Key and Token access [this link](https://trello.com/app-key) **after** signing in into trello

## ENV variables and secrets

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### You will have to modify the `.env` to include the following variables and populate them accordingly.

```bash 
#save your secrets in .env
TRELLO_API_KEY=<your-trello-API-key>
TRELLO_TOKEN=<your-trello-token>
# we will also add a variable for the trello board_id value so it can be modified to the user's will.
BOARD_ID=<trello-board-id> 
```
_The `.env` file will be ignored by git (see: [`.gitignore`](.gitignore))_
## Running the App locally

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

## Testing

You can run the test modules by running:
``` bash
poetry run pytest .
# or 
poetry run pytest <path-to-specific-test-file>
```

## Running the App in Docker
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
