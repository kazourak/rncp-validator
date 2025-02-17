# RNCP Validator ✨

Welcome to the RNCP Validator project! This tool helps you identify commits made outside of school hours by comparing them with a provided calendar.

## 📅 How to Get the Calendar

You can download the calendar by clicking on the "Télécharger le calendrier" button in the "Calendrier" section at [CFA 42](https://cfa.42.fr/students/calendars). The calendar must be a `.xlsx` file.

## 🔧 Basic Usage

### For Customers

1. **Install the Project**

   You can install the project directly from the main branch of the GitHub repository using the following command:

   ```sh
   pip install git+https://github.com/kazourak/rncp-validator.git
   ```

   To install a specific tagged version, use:

   ```sh
   pip install git+https://github.com/kazourak/rncp-validator.git@<tag_version>
   ```


2. **Run the Validator**

   Use the following command to analyze your calendar and Git repositories:

   ```sh
   rncp_validator <calendar.xlsx or dir> <list of .git paths>
   ```

   - **Example**: `rncp_validator path/to/calendar.xlsx path/to/.git`

   - **Directory of Calendars**: If you provide a directory, the program will analyze each `.xlsx` file within it.

   - **Multiple Git Paths**: You can provide multiple Git paths to analyze them all at once.

### For Developers

1. **Set Up the Environment**

   Create a virtual environment and install the requirements:

   ```sh
   make create_env
   source .venv/bin/activate
   make req
   ```

2. **Lint and Format the Code**

   Ensure your code adheres to style guidelines:

   ```sh
   make lint
   make format
   ```

3. **Run the Validator**

   You can run the validator with additional options:

   ```sh
   python rncp_validator/checker.py <calendar.xlsx or dir> <list of .git paths> --branch <branch_name> --not_recursive
   ```

   - **`--branch <branch_name>`**: Specify the branch to check.
   - **`--not_recursive`**: Do not explore the directory recursively.

## 📜 Command Reference

```sh
usage: checker.py [-h] [--branch BRANCH] [--not_recursive] calendar_path git_paths [git_paths ...]

Process calendar and git parse arguments.

positional arguments:
  calendar_path    Path to the calendar file or directory
  git_paths        Git paths arguments

options:
  -h, --help       show this help message and exit
  --branch BRANCH  Branch to check
  --not_recursive  Do not explore the directory recursively.
```

## 👥 Developers

We would like to express our gratitude to the following developers who have contributed to the RNCP Validator project:

![kazourak's avatar](https://avatars.githubusercontent.com/u/109950841?v=4&s=60) ![farinaleo's avatar](https://avatars.githubusercontent.com/u/46383251?v=4&s=60) 

## 🛠️ Makefile Commands

- **`make install`**: Install the project.
- **`make create_env`**: Create a virtual environment.
- **`make req`**: Install requirements.
- **`make lint`**: Lint the code using `flake8` and `black`.
- **`make format`**: Format the code using `black`.

---