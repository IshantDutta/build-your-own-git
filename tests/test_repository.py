
import os

from mini_git.repository import init_repository


def test_repository_initialization(tmp_path, monkeypatch):

    # Run the test inside a temporary directory
    monkeypatch.chdir(tmp_path)

    init_repository()

    # Check repository directories
    assert os.path.isdir(".mygit")
    assert os.path.isdir(".mygit/objects")
    assert os.path.isdir(".mygit/refs")
    assert os.path.isdir(".mygit/refs/heads")

    # Check repository files
    assert os.path.isfile(".mygit/HEAD")
    assert os.path.isfile(".mygit/config")


def test_head_content(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    init_repository()

    with open(".mygit/HEAD", "r") as file:
        content = file.read()

    assert content == "ref: refs/heads/main\n"


def test_duplicate_initialization(tmp_path, monkeypatch, capsys):

    monkeypatch.chdir(tmp_path)

    init_repository()

    init_repository()

    output = capsys.readouterr()

    assert "Repository already exists" in output.out
