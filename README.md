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
Install the virtual environment:
```shell
poetry install
```
Install the pre-commit hooks:
```shell
poetry run pre-commit install
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
Head to the swagger page at [http://localhost:8000](http://localhost:8000) and try out the `/api/examples/wait` endpoint. Grab the `task_id` from the response, and use it to check the task status with the `/api/tasks/status` endpoint.

Stop the containers using
```shell
make stop
```

### Notes
This example uses [Azure Blob Storage](https://docs.celeryq.dev/en/stable/internals/reference/celery.backends.azureblockblob.html) for the task results back end and (temporarily) [Redis](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html) for the message broker. Once [this commit](https://github.com/celery/kombu/commit/b3e89101dc6a4a002ec48a756ab82589da1c7541) is released by kombu, [Azure Storage Queues](https://docs.celeryq.dev/projects/kombu/en/latest/reference/kombu.transport.azurestoragequeues.html) can be used for the message broker. [Azurite](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio) is used for local Azure Storage emulation.
