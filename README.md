# fastapi-celery-example
An example [FastAPI](https://fastapi.tiangolo.com/) app using [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) and [Azure storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview) for task queuing.

[![CI](https://github.com/davidbossanyi/python-template/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/davidbossanyi/python-template/actions/workflows/ci.yaml)

### Requirements
 - [make](https://www.gnu.org/software/make/) (e.g. from [chocolatey](https://community.chocolatey.org/packages/make) on Windows)
 - [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)
 - [python](https://www.python.org/downloads/) 3.10 or higher
 - [poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) 1.3 or higher

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
make test
```
Run the linters:
```shell
make lint
```

#### Running the application
Spin up the docker containers using
```shell
make start
```
The swagger page will be launched in your browser. Try out the `/api/run/wait` endpoint. Grab the `task_id` from the response, and use it to check the task status with the `/api/tasks/status` endpoint.

Stop the containers using
```shell
make stop
```
