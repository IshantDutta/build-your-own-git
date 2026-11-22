
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
