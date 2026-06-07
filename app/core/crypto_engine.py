import os
import struct
import zipfile
import tempfile
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag


MAGIC = b"VAULTIX2"
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
CHUNK_SIZE = 1024 * 1024 * 4  # 4 MB chunks


class CryptoError(Exception):
    pass


def derive_key(password: str, salt: bytes) -> bytes:
    if not password or len(password) < 8:
        raise CryptoError("Password must be at least 8 characters.")

    kdf = Scrypt(
        salt=salt,
        length=KEY_SIZE,
        n=2**14,
        r=8,
        p=1,
    )

    return kdf.derive(password.encode("utf-8"))


def encrypt_file(input_path: str, output_path: str, password: str) -> str:
    source = Path(input_path)

    if not source.exists() or not source.is_file():
        raise CryptoError("Input file does not exist.")

    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    original_name = source.name.encode("utf-8")

    try:
        with open(source, "rb") as infile, open(output_path, "wb") as outfile:
            outfile.write(MAGIC)
            outfile.write(struct.pack(">H", len(original_name)))
            outfile.write(original_name)
            outfile.write(salt)

            chunk_index = 0

            while True:
                chunk = infile.read(CHUNK_SIZE)

                if not chunk:
                    break

                nonce = os.urandom(NONCE_SIZE)
                aad = MAGIC + original_name + struct.pack(">Q", chunk_index)

                encrypted_chunk = aesgcm.encrypt(nonce, chunk, aad)

                outfile.write(nonce)
                outfile.write(struct.pack(">I", len(encrypted_chunk)))
                outfile.write(encrypted_chunk)

                chunk_index += 1

    except Exception as e:
        raise CryptoError(f"Encryption failed: {e}")

    return output_path


def decrypt_file(input_path: str, output_folder: str, password: str) -> str:
    encrypted_path = Path(input_path)

    if not encrypted_path.exists() or not encrypted_path.is_file():
        raise CryptoError("Encrypted file does not exist.")

    try:
        with open(encrypted_path, "rb") as infile:
            magic = infile.read(len(MAGIC))

            if magic != MAGIC:
                raise CryptoError("Invalid or old Vaultix encrypted file.")

            name_length_data = infile.read(2)
            name_length = struct.unpack(">H", name_length_data)[0]

            original_name_bytes = infile.read(name_length)
            original_name = original_name_bytes.decode("utf-8")

            salt = infile.read(SALT_SIZE)

            key = derive_key(password, salt)
            aesgcm = AESGCM(key)

            output_path = Path(output_folder) / original_name

            with open(output_path, "wb") as outfile:
                chunk_index = 0

                while True:
                    nonce = infile.read(NONCE_SIZE)

                    if not nonce:
                        break

                    chunk_size_data = infile.read(4)

                    if len(chunk_size_data) != 4:
                        raise CryptoError("Corrupted encrypted file.")

                    encrypted_chunk_size = struct.unpack(">I", chunk_size_data)[0]
                    encrypted_chunk = infile.read(encrypted_chunk_size)

                    if len(encrypted_chunk) != encrypted_chunk_size:
                        raise CryptoError("Corrupted encrypted file.")

                    aad = MAGIC + original_name_bytes + struct.pack(">Q", chunk_index)

                    try:
                        decrypted_chunk = aesgcm.decrypt(
                            nonce,
                            encrypted_chunk,
                            aad,
                        )
                    except InvalidTag:
                        raise CryptoError("Wrong password or file was modified.")

                    outfile.write(decrypted_chunk)
                    chunk_index += 1

    except CryptoError:
        raise
    except Exception as e:
        raise CryptoError(f"Decryption failed: {e}")

    return str(output_path)


def zip_folder(folder_path: str, zip_path: str) -> None:
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise CryptoError("Folder does not exist.")

    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        allowZip64=True,
    ) as zip_file:
        for file in folder.rglob("*"):
            if file.is_file():
                zip_file.write(file, file.relative_to(folder.parent))


def encrypt_folder(folder_path: str, output_path: str, password: str) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        folder_name = Path(folder_path).name
        temp_zip = Path(temp_dir) / f"{folder_name}.zip"

        zip_folder(folder_path, str(temp_zip))

        return encrypt_file(str(temp_zip), output_path, password)


def decrypt_folder(input_path: str, output_folder: str, password: str) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        decrypted_zip = decrypt_file(input_path, temp_dir, password)

        extract_path = Path(output_folder)

        with zipfile.ZipFile(decrypted_zip, "r") as zip_file:
            zip_file.extractall(extract_path)

        return str(extract_path)