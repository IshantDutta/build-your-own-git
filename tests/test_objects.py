import os
import pytest

from mini_git.objects import sha1_hash
from mini_git.objects import git_object_hash
from mini_git.objects import store_blob, read_blob
from mini_git.objects import store_file


def test_sha1_known_value():

    result = sha1_hash(b"abc")

    assert result == "a9993e364706816aba3e25717850c26c9cd0d89d"


def test_sha1_empty_content():

    result = sha1_hash(b"")

    assert result == "da39a3ee5e6b4b0d3255bfef95601890afd80709"


def test_identical_content_same_hash():

    file_a = b"Hello World"
    file_b = b"Hello World"

    assert sha1_hash(file_a) == sha1_hash(file_b)


def test_different_content_different_hash():

    file_a = b"Hello World"
    file_b = b"Hello Git"

    assert sha1_hash(file_a) != sha1_hash(file_b)


def test_binary_content():

    binary_data = bytes([0, 1, 2, 3, 255])

    result = sha1_hash(binary_data)

    assert len(result) == 40


def test_invalid_input():

    with pytest.raises(TypeError):
        sha1_hash("Hello")




def test_empty_blob_hash():

    result = git_object_hash(b"")

    # Known Git SHA-1 hash of an empty blob
    assert result == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


def test_git_object_hash_format():

    result = git_object_hash(b"Hello")

    assert len(result) == 40


def test_git_hash_differs_from_raw_hash():

    data = b"Hello"

    raw_hash = sha1_hash(data)
    object_hash = git_object_hash(data)

    assert raw_hash != object_hash


def test_different_object_types_produce_different_hashes():

    data = b"Hello"

    blob_hash = git_object_hash(data, "blob")
    tree_hash = git_object_hash(data, "tree")

    assert blob_hash != tree_hash


def test_invalid_object_type():

    with pytest.raises(ValueError):
        git_object_hash(b"Hello", "invalid")


def test_git_object_rejects_string():

    with pytest.raises(TypeError):
        git_object_hash("Hello")




def test_store_and_read_blob(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    data = b"Hello World"

    object_hash = store_blob(data)

    retrieved_data = read_blob(object_hash)

    assert retrieved_data == data


def test_store_empty_blob(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    object_hash = store_blob(b"")

    assert read_blob(object_hash) == b""


def test_store_binary_blob(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    data = bytes([0, 1, 2, 3, 255])

    object_hash = store_blob(data)

    assert read_blob(object_hash) == data


def test_identical_blobs_share_object(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    data = b"Hello World"

    hash_a = store_blob(data)
    hash_b = store_blob(data)

    assert hash_a == hash_b

    object_path = os.path.join(
        ".mygit", "objects", hash_a[:2], hash_a[2:]
    )

    assert os.path.isfile(object_path)


def test_missing_blob(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    with pytest.raises(FileNotFoundError):
        read_blob("a" * 40)




def test_store_text_file(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    file_path = tmp_path / "hello.txt"
    file_path.write_bytes(b"Hello World")

    object_hash = store_file(str(file_path))

    assert read_blob(object_hash) == b"Hello World"


def test_store_binary_file(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    os.makedirs(".mygit/objects")

    binary_data = bytes([0, 1, 2, 3, 255])

    file_path = tmp_path / "image.bin"
    file_path.write_bytes(binary_data)

    object_hash = store_file(str(file_path))

    assert read_blob(object_hash) == binary_data


def test_store_missing_file():

    with pytest.raises(FileNotFoundError):
        store_file("nonexistent_file.txt")
