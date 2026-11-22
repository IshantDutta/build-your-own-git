
from mini_git.repository import init_repository


def execute_command(command):

    if command == "init":
        init_repository()

    else:
        print(f"Unknown command: {command}")
