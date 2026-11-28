
import hashlib
import os
import zlib


def sha1_hash(data: bytes) -> str:
    """
    Generate a SHA-1 hash for the given data.

    Args:
        data: Content in bytes.

    Returns:
        A 40-character hexadecimal SHA-1 hash.
    """

    # Ensure that the input is in bytes
    if not isinstance(data, bytes):
        raise TypeError("SHA-1 input must be bytes")

    # Generate the SHA-1 hash
    hash_object = hashlib.sha1(data)

    # Convert the digest into hexadecimal representation
    return hash_object.hexdigest()


def git_object_hash(data: bytes, object_type: str = "blob") -> str:
    """
    Generate a Git-compatible SHA-1 object hash.

    Args:
        data: Object content in bytes.
        object_type: Type of Git object.

    Returns:
        A 40-character hexadecimal SHA-1 hash.
    """

    # Validate the content
    if not isinstance(data, bytes):
        raise TypeError("Object content must be bytes")

    # Validate the object type
    valid_types = ("blob", "tree", "commit", "tag")

    if object_type not in valid_types:
        raise ValueError("Invalid Git object type")

    # Calculate the content size in bytes
    content_size = len(data)

    # Construct the Git object header
    header = f"{object_type} {content_size}".encode("ascii")

    # Combine header, null byte and actual content
    full_object = header + b"\0" + data

    # Generate SHA-1 hash of the complete object
    return sha1_hash(full_object)


def store_blob(data: bytes) -> str:
    """
    Store a blob object inside .mygit/objects.

    Returns:
        The SHA-1 object ID.
    """

    if not isinstance(data, bytes):
        raise TypeError("Blob content must be bytes")

    # Generate the Git-compatible object hash
    object_hash = git_object_hash(data, "blob")

    # Construct the Git object representation
    header = f"blob {len(data)}".encode("ascii")
    full_object = header + b"\0" + data

    # Compress the complete object
    compressed_object = zlib.compress(full_object)

    # Split the hash into directory and filename
    directory_name = object_hash[:2]
    file_name = object_hash[2:]

    # Construct the object directory path
    object_directory = os.path.join(
        ".mygit", "objects", directory_name
    )

    # Create the directory if it doesn't exist
    os.makedirs(object_directory, exist_ok=True)

    # Construct the final object path
    object_path = os.path.join(
        object_directory, file_name
    )

    # Avoid rewriting an existing object
    if not os.path.exists(object_path):
        with open(object_path, "wb") as object_file:
            object_file.write(compressed_object)

    print(f"Blob stored: {object_hash}")

    return object_hash


def read_blob(object_hash: str) -> bytes:
    """
    Retrieve and decompress a stored blob.

    Returns:
        Original blob content in bytes.
    """

    # Validate the object hash
    if (
        not isinstance(object_hash, str)
        or len(object_hash) != 40
        or any(c not in "0123456789abcdef" for c in object_hash)
    ):
        raise ValueError("Invalid object hash")

    # Reconstruct the object path
    directory_name = object_hash[:2]
    file_name = object_hash[2:]

    object_path = os.path.join(
        ".mygit", "objects", directory_name, file_name
    )

    # Check whether the object exists
    if not os.path.isfile(object_path):
        raise FileNotFoundError("Blob object not found")

    # Read compressed data
    with open(object_path, "rb") as object_file:
        compressed_data = object_file.read()

    # Decompress the object
    full_object = zlib.decompress(compressed_data)

    # Separate header and content
    header, content = full_object.split(b"\0", 1)

    # Extract object type and size
    object_type, object_size = header.split(b" ", 1)

    # Verify object type
    if object_type != b"blob":
        raise ValueError("Object is not a blob")

    # Verify content size
    if len(content) != int(object_size):
        raise ValueError("Blob size mismatch")

    # Verify object integrity
    if git_object_hash(content, "blob") != object_hash:
        raise ValueError("Blob hash verification failed")

    return content
