
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
