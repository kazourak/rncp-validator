"""Checker to identify commits not done on school time."""

import argparse

from git import Repo
from openpyxl import load_workbook

from rncp_validator.Calendar import Calendar


def get_all_commits(git_path: str, branch: str = None) -> dict:
    """
    Get from the given git path all the commits from the head.
    :param git_path: The .git path.
    :param branch: The branch to check.
    :return: All commits as a dict the hexa as key and the date as value.
    """
    commits = dict()

    repo = Repo(git_path)

    if branch not in repo.branches:
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
        parser.add_argument("calendar_path", type=str, help="Path to the calendar file")
        parser.add_argument("git_parse", type=str, help="Git parse argument")
        parser.add_argument("--branch", type=str, default=None, help="Branch to check")

        args = parser.parse_args()

        cl = Calendar(load_workbook(args.calendar_path))
        cl.get_periods()

        commit_list = get_all_commits(args.git_parse, branch=args.branch)

        for commits in commit_list:
            if cl.date_in_period(commit_list[commits]):
                print("\033[92m" + "Commit", commits, "is in a school period" + "\033[0m")
            else:
                print("\033[91m" + "Commit", commits, "is not in a school period" + "\033[0m")
    except Exception as e:
        raise ValueError("{Find an error}") from e


if __name__ == "__main__":
    main()
