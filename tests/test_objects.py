
import pytest

from mini_git.objects import sha1_hash


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


from mini_git.objects import git_object_hash


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
