
import os


# Name of our internal Git directory
REPO_DIR = ".mygit"


def init_repository():
    """
    Initialize a new mini-git repository
    in the current working directory.
    """

    # Check whether a repository already exists
    if os.path.exists(REPO_DIR):
        print("Error: Repository already exists.")
        return

    # Create the main repository directory
    os.makedirs(REPO_DIR)

    # Create the objects directory
    os.makedirs(os.path.join(REPO_DIR, "objects"))

    # Create refs/heads directory
    os.makedirs(os.path.join(REPO_DIR, "refs", "heads"))

    # Create HEAD file
    head_path = os.path.join(REPO_DIR, "HEAD")

    with open(head_path, "w") as head_file:
        head_file.write("ref: refs/heads/main\n")

    # Create config file
    config_path = os.path.join(REPO_DIR, "config")

    with open(config_path, "w") as config_file:
        config_file.write("[core]\n")
        config_file.write("\trepositoryformatversion = 0\n")
        config_file.write("\tbare = false\n")

    print("Initialized empty Mini Git repository.")
