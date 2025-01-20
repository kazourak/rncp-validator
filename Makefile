.PHONY: create_env
create_env: ## Create a virtual env
	@python -m venv .venv
	@echo venv created run source .venv/bin/activate

.PHONY: install
install: requirements.txt ## Install the requirements.txt
	@pip install -r requirements.txt

.PHONY: lint
lint: ## Lint using flake8 and black
	flake8 . --disable-noqa
	isort --check --diff --profile black .
	black pyproject.toml .


.PHONY: format
format: ## Format source code with black
	black .
	isort . --profile black