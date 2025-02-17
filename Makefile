PROJECT_NAME=rncp_validator

.PHONY: create_env
create_env:
	@python -m venv .venv
	@echo venv created run source .venv/bin/activate

.PHONY: req
req:
	@pip install -r requirements.txt
	@pip install -e .

.PHONY: install
install:
	@echo -n "\033[90m"
	@pip install -e .
	@if [ $$? -ne 0 ]; then \
		echo -n "\033[0m"; \
		echo "\033[1;31m✖ Error: Project installation failed. Please check the output above for details.\033[0m"; \
		exit 1; \
	fi
	@echo -n "\033[0m"
	@echo "\n\033[1;32m✔ Project installed successfully! ✨\033[0m\n"
	@echo "\033[1m--------------------------\033[0m"
	@echo "\033[1m       Project Setup       \033[0m"
	@echo "\033[1m--------------------------\033[0m\n"
	@echo "To use the project, follow these steps:\n"
	@echo "\033[1;34m1. Navigate to the project directory.\033[0m"
	@echo "\033[1;34m2. Run the command: \`${PROJECT_NAME} <calendar path> <git path>\`\033[0m\n"
	@echo "For more details, use: \`${PROJECT_NAME} --help\`\n"
	@python -m ${PROJECT_NAME} --help




.PHONY: lint
lint: ## Lint using flake8 and black
	flake8 ${PROJECT_NAME} --max-line-length 99
	isort --check --diff --profile black ${PROJECT_NAME}
	black --check ${PROJECT_NAME} --line-length 99


.PHONY: format
format: ## Format source code with black
	black ${PROJECT_NAME}  --line-length 99
	isort ${PROJECT_NAME} --profile black