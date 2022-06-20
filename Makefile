.DEFAULT_GOAL := show-help
.PHONY: show-help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
## This help screen
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)";echo;sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## //;td" -e"s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=29 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'

.PHONY: test-all
## Run all tests
test-all: test-unit pre-integration test-integration post-integration

.PHONY: test-unit
## Run unit tests
test-unit:
	poetry run pytest tests/ -m "not integration"

.PHONY: pre-integration
## Spin up docker containers for integration tests
pre-integration:
	docker-compose -f docker-compose-pytest.yaml up -d --remove-orphans

.PHONY: post-integration
## Spin down docker containers for integration tests
post-integration:
	docker-compose -f docker-compose-pytest.yaml down

.PHONY: test-integration
## Run integration tests
test-integration: pre-integration
	poetry run pytest tests -m "integration"

.PHONY: run
## Spin up all containers locally, including api and worker
run:
	docker-compose -f docker-compose-dev.yaml up -d --build --remove-orphans
	python -m webbrowser "http://localhost:8000"

.PHONY: stop
## Spin down all containers locally, including api and worker
stop:
	docker-compose -f docker-compose-dev.yaml down

.PHONY: lint
## Lint the project (and fix)
lint:
	poetry run pre-commit run --all-files
