"""Checker to identify commits not done on school time."""

import argparse
import glob
import os

from git import Repo
from openpyxl import load_workbook

from rncp_validator.Calendar import Calendar


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


def analyse(calendar_path: str, git_path: str, branch: str = None):
    """
    Check for if the given git history match with the calendar.
    :param calendar_path: The path to the calendar as a xlsx file.
    :param git_path: The .git path.
    :param branch: The branch to check.
    :return: None
    """
    cl = Calendar(load_workbook(calendar_path))
    cl.get_periods()

    commit_list = get_all_commits(git_path, branch=branch)

    for commits in commit_list:
        if cl.date_in_period(commit_list[commits]):
            print(
                "\033[92m" + "Commit",
                commits,
                "at",
                commit_list[commits],
                "is in a school period" + "\033[0m",
            )
        else:
            print(
                "\033[91m" + "Commit",
                commits,
                "at",
                commit_list[commits],
                "is not in a school period" + "\033[0m",
            )


def get_all_commits(git_path: str, branch: str = None) -> dict:
    """
    Get from the given git path all the commits from the head.
    :param git_path: The .git path.
    :param branch: The branch to check.
    :return: All commits as a dict the hexa as key and the date as value.
    """
    commits = dict()

    repo = Repo(git_path)

    if branch and branch not in repo.branches:
        raise ValueError(
            f"Branch '{branch}' does not exist in the repository."
            + f" Possible choice {[branch.name for branch in repo.branches]}"
        )
    print(f"Working on all commits from {repo.active_branch.name if not branch else branch}...")

    for commit in repo.iter_commits(repo.active_branch.name if not branch else branch):
        commits[commit.hexsha] = commit.committed_datetime

    return commits


def main():
    """
    Main program.
    :return:
    :rtype:
    """
    try:
        parser = argparse.ArgumentParser(description="Process calendar and git parse arguments.")
        parser.add_argument(
            "calendar_path", type=str, help="Path to the calendar file or directory"
        )
        parser.add_argument("git_parse", type=str, help="Git parse argument")
        parser.add_argument("--branch", type=str, default=None, help="Branch to check")
        parser.add_argument(
            "--not_recursive",
            action="store_false",
            help="Do not explore the directory recursively.",
        )

        args = parser.parse_args()

        xlsx_paths = get_calendars(args.calendar_path, args.not_recursive)

        for xlsx_path in xlsx_paths:
            analyse(xlsx_path, args.git_parse, args.branch)

    except Exception as e:
        raise ValueError("{Find an error}") from e


if __name__ == "__main__":
    main()
