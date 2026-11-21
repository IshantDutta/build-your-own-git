
import sys

from mini_git.commands import execute_command


def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <command>")
        return

    command = sys.argv[1]

    execute_command(command)


if __name__ == "__main__":
    main()
