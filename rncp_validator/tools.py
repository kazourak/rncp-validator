import glob
import os
import uuid
from datetime import datetime

from git import Repo

MONTH_TO_NB = {
    "Janvier": "01",
    "Février": "02",
    "Mars": "03",
    "Avril": "04",
    "Mai": "05",
    "Juin": "06",
    "Juillet": "07",
    "Août": "08",
    "Septembre": "09",
    "Octobre": "10",
    "Novembre": "11",
    "Décembre": "12",
}


def clone_repo(repo_url: str, clone_path: str) -> Repo:
    """
    Clone a repository from a given URL to a specified local path.
    :param repo_url: The URL of the repository to clone.
    :param clone_path: The local path where the repository should be cloned.
    :return: The cloned repository as a Repo object.
    """
    if not os.path.exists(clone_path):
        os.makedirs(clone_path)
    return Repo.clone_from(repo_url, clone_path)


def get_all_commits(git_path: str, branch: str = None) -> dict:
    """
    Get from the given git path all the commits from the head.
    :param git_path: The .git path.
    :param branch: The branch to check.
    :return: All commits as a dict with the hexa as key and a tuple (date, author) as value.
    """
    commits = dict()

    if (
        git_path.startswith("https://")
        or git_path.startswith("http://")
        or git_path.startswith("git@")
    ):
        repo = clone_repo(git_path, "/tmp/rncp-validator/" + str(uuid.uuid4()))
    else:
        repo = Repo(git_path)

    if branch and branch not in repo.branches:
        raise ValueError(
            f"Branch '{branch}' does not exist in the repository."
            + f" Possible choice {[branch.name for branch in repo.branches]}"
        )
    print(
        "\033[1m"
        + f"Working on all commits from {repo.active_branch.name if not branch else branch}..."
        + "\033[0m"
    )

    for commit in repo.iter_commits(repo.active_branch.name if not branch else branch):
        commits[commit.hexsha] = (commit.committed_datetime, commit.author.name)

    return commits


def get_calendars(source_path: str, recursive: bool = False) -> list[str]:
    """
    Get all possible paths that match with xlsx files. If the source is a
    file the function returns it in a list, else, if the source is a dir,
    the function extracts all xlsx files from it.
    :param source_path: The source path.
    :param recursive: Explore the directory recursively.
    :return: A list of xlsx files.
    """
    if os.path.isfile(source_path) and source_path.endswith(".xlsx"):
        return [os.path.normpath(source_path)]
    if os.path.isdir(source_path):
        return glob.glob(os.path.join(source_path, "**", "*.xlsx"), recursive=recursive)


def to_date(month_str: str, day_str: str, year_str: str) -> datetime:
    """
    Convert the given arguments, month, day and year into a datetime object.
    :param month_str: The mount number as a string.
    :param day_str: The day number as a string.
    :param year_str: The year as a string.
    :return: The datetime object.
    """
    return datetime(int(year_str), int(month_str), int(day_str))
