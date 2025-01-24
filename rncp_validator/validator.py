import subprocess
import os


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
            ["git", "-C", repo_path, "rebase", "-i", f"{commit_hash}^"],
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


# Exemple d'utilisation
if __name__ == "__main__":
    # Chemin du repo Git
    repo_path = "/Users/nolanskiba/Documents/Ftl_quantum/"

    # Hash du commit à modifier
    commit_hash = "7ad4ec1181183cd0aefc64b614b03e362aaf61c1"

    # Nouvelle date au format "YYYY-MM-DD HH:MM:SS"
    new_date = "2026-01-01 12:34:56"

    change_commit_date(repo_path, commit_hash, new_date)
