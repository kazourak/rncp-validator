PROJECT_NAME=rncp_validator

.PHONY: create_env
create_env:
	@python -m venv .venv
	@echo venv created run source .venv/bin/activate

.PHONY: install
install:
	@pip install -r requirements.txt
	@pip install -e .

.PHONY: lint
lint: ## Lint using flake8 and black
	flake8 ${PROJECT_NAME} --max-line-length 99
	isort --check --diff --profile black ${PROJECT_NAME}
	black --check ${PROJECT_NAME} --line-length 99


.PHONY: format
format: ## Format source code with black
	black ${PROJECT_NAME}  --line-length 99
	isort ${PROJECT_NAME} --profile black