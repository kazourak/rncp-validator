import argparse
from git import Repo
from openpyxl import load_workbook
from Calendar import Calendar


def get_all_commits(git_path):
    commits = dict()

    repo = Repo(git_path)

    for commit in repo.iter_commits():
        commits[commit.hexsha] = commit.committed_datetime

    return commits


def main():
    parser = argparse.ArgumentParser(description='Process calendar and git parse arguments.')
    parser.add_argument('calendar_path', type=str, help='Path to the calendar file')
    parser.add_argument('git_parse', type=str, help='Git parse argument')

    args = parser.parse_args()

    cl = Calendar(load_workbook(args.calendar_path))
    cl.get_periods()

    commit_list = get_all_commits(args.git_parse)

    for commits in commit_list:
        if cl.date_in_period(commit_list[commits]):
            print('\033[92m' + 'Commit', commits, 'is in a school period' + '\033[0m')
        else:
            print('\033[91m' + 'Commit', commits, 'is not in a school period' + '\033[0m')


if __name__ == "__main__":
    main()
