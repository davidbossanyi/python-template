# fastapi-celery-example
An example [FastAPI](https://fastapi.tiangolo.com/) app using [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) for task queuing.

[![CI](https://github.com/davidbossanyi/python-template/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/davidbossanyi/python-template/actions/workflows/ci.yaml)

### Requirements
 - [make](https://www.gnu.org/software/make/) (e.g. from [chocolatey](https://chocolatey.org/) on Windows)
 - [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)
 - [python](https://www.python.org/downloads/release/python-3912/) 3.9 or higher
 - [poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) 1.1 or higher

### Running locally
#### Getting set up
Clone the repo:
```shell
git clone https://github.com/davidbossanyi/fastapi-celery-example.git
```
Install the virtual environment and pre-commit hooks:
```shell
make init
```
Run the tests:
```shell
make test-all
```
Run the linters:
```shell
make lint
```

#### Running the application
Spin up the docker containers using
```shell
make run
```
The swagger page will be launched at [http://localhost:8000](http://localhost:8000). Try out the `/api/examples/wait` endpoint. Grab the `task_id` from the response, and use it to check the task status with the `/api/tasks/status` endpoint.

Stop the containers using
```shell
make stop
```

### Notes
Currently waiting for [this commit](https://github.com/celery/kombu/commit/0e57a7b3a0edde7bad7061e73f741296ce06c3c8) to make its way into a kombu release. This will allow the integration tests to pass.
