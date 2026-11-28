
import hashlib


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
