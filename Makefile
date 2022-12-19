ifdef OS
   .DEFAULT_GOAL := help-ps
else
   .DEFAULT_GOAL := help-sh
endif

.PHONY: help-ps
## Show this help screen (powershell)
help-ps:
	@powershell "Write-Host 'Available Rules:' -ForegroundColor Blue; Write-Host ''; Get-Content Makefile | Select-String -Pattern '^##\s|^\.PHONY:\s' | ForEach-Object {if($$_.Line.StartsWith('.PHONY')) {Write-Host $$_.Line.Replace('.PHONY: ', '').PadRight(29) -NoNewLine -ForegroundColor Yellow} else {Write-Host $$_.Line.Replace('##', '') -ForegroundColor Green}}"

.PHONY: help-sh
## Show this help screen (unix)
help-sh:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)";echo;sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## //;td" -e"s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=19 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'|more

.PHONY: test
## Run all tests
test: test-unit pre-integration test-integration post-integration

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
test-integration:
	poetry run pytest tests -m "integration"

.PHONY: run
## Spin up all containers locally, including api and worker
run:
	docker-compose -f docker-compose-dev.yaml up -d --build --remove-orphans
	python -m webbrowser -t "http://localhost:8000"

.PHONY: stop
## Spin down all containers locally, including api and worker
stop:
	docker-compose -f docker-compose-dev.yaml down

.PHONY: lint
## Lint the project (and fix)
lint:
	poetry run pre-commit run --all-files

.PHONY: init
## Initialize the project
init:
	poetry install && poetry run pre-commit install
