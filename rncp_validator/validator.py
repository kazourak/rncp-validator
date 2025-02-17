import argparse
import itertools
import os
import subprocess
from datetime import date, datetime

from openpyxl import load_workbook

from rncp_validator.Calendar import Calendar
from rncp_validator.checker import get_bad_commits
from rncp_validator.tools import get_calendars


def change_commit_date(repo_path, commit_hash, new_date):
    """
    Change la date d'un commit spécifique dans un dépôt Git.

    :param repo_path: Chemin du dépôt Git
    :param commit_hash: Hash du commit à modifier
    :param new_date: Nouvelle date au format "YYYY-MM-DD HH:MM:SS"
    """
    # Vérifiez si le chemin est un dépôt Git valide
    try:
        subprocess.run(
            ["git", "-C", repo_path, "rev-parse"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        print(f"Erreur : Le chemin '{repo_path}' n'est pas un dépôt Git valide.")
        return

    # Étape 1 : Lancez le rebase interactif jusqu'au parent du commit cible
    try:
        print(f"Lancement du rebase interactif pour modifier le commit {commit_hash}...")
        rebase_process = subprocess.run(
            ["git", "-C", repo_path, "rebase", f"{commit_hash}^"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"Erreur pendant le rebase interactif : {e.stderr.decode()}")
        return

    # Étape 2 : Modifier la date du commit
    try:
        # Définissez les variables d'environnement pour la nouvelle date
        os.environ["GIT_AUTHOR_DATE"] = new_date
        os.environ["GIT_COMMITTER_DATE"] = new_date

        # Réamendez le commit avec la nouvelle date
        subprocess.run(
            ["git", "-C", repo_path, "commit", "--amend", "--no-edit", "--date", new_date],
            check=True,
        )

        # Continuez le rebase
        subprocess.run(["git", "-C", repo_path, "rebase", "--continue"], check=True)

        print(f"Date du commit {commit_hash} modifiée avec succès à {new_date}.")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la modification de la date : {e.stderr.decode()}")
        return



def get_commits_and_suggested_date(commits: dict, calendar_path: str) -> dict:
    """
    Get all commits with a suggested date that match the school periods.
    :param commits: Dict with all identified commits to change.
    :param calendar_path: Calendar path.
    :return: The commits dict with a third value corresponding to the suggested date.
    """
    suggested_date = {}
    cl = Calendar(load_workbook(calendar_path))
    cl.get_periods()

    print("We have to edit this commits :")

    for bad_commit in commits:
        _new_date = cl.nearest_date(datetime.combine(commits[bad_commit][0], datetime.min.time()))
        print(
            f"sha {bad_commit}: date {commits[bad_commit][0]}, user {commits[bad_commit][1]},"
            + f" new possible date {_new_date}"
        )
        suggested_date[bad_commit] = (commits[bad_commit][0], commits[bad_commit][1], _new_date)

    return suggested_date


def ask_and_change_commit_dates(repo_path: str, suggested_date: dict):
    """
    Ask the user for each commit whether they want to change its date, and apply changes if confirmed.

    :param repo_path: Path to the Git repository.
    :param suggested_date: Dictionary with commit hashes as keys and tuples (old_date, user, new_date) as values.
    """
    for commit_hash, (old_date, user, new_date) in suggested_date.items():
        print(f"\nCommit: {commit_hash}")
        print(f"User: {user}")
        print(f"Current Date: {old_date}")
        print(f"Suggested New Date: {new_date}")

        # Ask the user if they want to change the commit date
        user_input = input("Do you want to change the commit date? (y/n): ").strip().lower()

        if user_input == "y":
            formatted_new_date = new_date.strftime(
                "%Y-%m-%d 10:00:00"
            )  # Ensure time is set to 10 AM
            change_commit_date(repo_path, commit_hash, formatted_new_date)
        else:
            print(f"Skipping commit {commit_hash}.")


def main():
    """
    Main program.
    """
    try:
        parser = argparse.ArgumentParser(
            description="Process calendar and git parse arguments to change the commit date."
        )
        parser.add_argument("calendar_path", type=str, help="Path to the calendar file (a .xlsx)")
        parser.add_argument("git_path", type=str, help="Git path argument")
        parser.add_argument("--branch", type=str, default=None, help="Branch to check")

        args = parser.parse_args()

        calendar_path = args.calendar_path
        repo_path = args.git_path

        if not os.path.isfile(calendar_path) and not calendar_path.endswith(".xlsx"):
            raise ValueError(f"Calendar path must be a .xlsx file but got {calendar_path}")

        bad_commits = get_bad_commits(calendar_path, repo_path, args.branch)

        if len(bad_commits) == 0:
            print("Nothing to change !")
            return

        suggested_date = get_commits_and_suggested_date(bad_commits, calendar_path)

        ask_and_change_commit_dates(repo_path, suggested_date)

    except Exception as e:
        raise ValueError("{Find an error}") from e


if __name__ == "__main__":
    main()
