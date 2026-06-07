import os
from pathlib import Path


class ShredderError(Exception):
    pass


def secure_delete(file_path: str, passes: int = 3):
    path = Path(file_path)

    if not path.exists():
        raise ShredderError("File does not exist.")

    if not path.is_file():
        raise ShredderError("Only files are supported.")

    file_size = path.stat().st_size

    try:
        with open(path, "r+b") as file:
            for _ in range(passes):
                file.seek(0)
                file.write(os.urandom(file_size))
                file.flush()
                os.fsync(file.fileno())

        path.unlink()

    except Exception as e:
        raise ShredderError(f"Secure delete failed: {e}")