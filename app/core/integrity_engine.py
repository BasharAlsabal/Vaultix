import hashlib
from pathlib import Path


CHUNK_SIZE = 1024 * 1024 * 4  # 4 MB


class IntegrityError(Exception):
    pass


def calculate_sha256(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise IntegrityError("File does not exist.")

    sha256 = hashlib.sha256()

    try:
        with open(path, "rb") as file:
            while True:
                chunk = file.read(CHUNK_SIZE)

                if not chunk:
                    break

                sha256.update(chunk)

    except Exception as e:
        raise IntegrityError(f"Failed to calculate hash: {e}")

    return sha256.hexdigest()


def verify_sha256(file_path: str, expected_hash: str) -> bool:
    expected_hash = expected_hash.strip().lower()

    if len(expected_hash) != 64:
        raise IntegrityError("Invalid SHA-256 hash length.")

    actual_hash = calculate_sha256(file_path)

    return actual_hash == expected_hash