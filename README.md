# How can I get the calendar ?

You can get the calendar by clicking on the "Télécharger le calendrier" button in the "Calendrier" at https://cfa.42.fr/students/calendars.
The calendar must be a .xlsx file.

# Usage:

_Run `make install ` to set up the project._

`python rncp_validator/checker.py <calendar.xlsx or dir> <list of .git path>`

_If you give to the script a directory of calendars, the program will analyse each xlsx files._

_You can also give to the script multiple .git paths to analyse all at once._

```shell
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