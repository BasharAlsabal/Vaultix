import os
import struct
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidTag


MAGIC = b"VAULTIX-HYBRID1"
AES_KEY_SIZE = 32
NONCE_SIZE = 12
CHUNK_SIZE = 1024 * 1024 * 4


class HybridError(Exception):
    pass


def load_public_key(public_key_path: str):
    path = Path(public_key_path)
    if not path.exists():
        raise HybridError("Public key file does not exist.")

    try:
        return serialization.load_pem_public_key(path.read_bytes())
    except Exception:
        raise HybridError("Invalid public key file.")


def load_private_key(private_key_path: str, password: str):
    path = Path(private_key_path)
    if not path.exists():
        raise HybridError("Private key file does not exist.")

    try:
        return serialization.load_pem_private_key(
            path.read_bytes(),
            password=password.encode("utf-8"),
        )
    except Exception:
        raise HybridError("Invalid private key or wrong password.")


def encrypt_for_receiver(input_path: str, public_key_path: str, output_path: str) -> str:
    source = Path(input_path)

    if not source.exists() or not source.is_file():
        raise HybridError("Input file does not exist.")

    public_key = load_public_key(public_key_path)

    aes_key = os.urandom(AES_KEY_SIZE)
    aesgcm = AESGCM(aes_key)

    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    original_name = source.name.encode("utf-8")

    try:
        with open(source, "rb") as infile, open(output_path, "wb") as outfile:
            outfile.write(MAGIC)
            outfile.write(struct.pack(">H", len(original_name)))
            outfile.write(original_name)
            outfile.write(struct.pack(">H", len(encrypted_aes_key)))
            outfile.write(encrypted_aes_key)

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

        return output_path

    except Exception as e:
        raise HybridError(f"Hybrid encryption failed: {e}")


def decrypt_from_sender(input_path: str, private_key_path: str, password: str, output_folder: str) -> str:
    package = Path(input_path)

    if not package.exists() or not package.is_file():
        raise HybridError("Hybrid package does not exist.")

    private_key = load_private_key(private_key_path, password)

    try:
        with open(package, "rb") as infile:
            magic = infile.read(len(MAGIC))

            if magic != MAGIC:
                raise HybridError("Invalid Vaultix hybrid package.")

            name_length = struct.unpack(">H", infile.read(2))[0]
            original_name_bytes = infile.read(name_length)
            original_name = original_name_bytes.decode("utf-8")

            encrypted_key_length = struct.unpack(">H", infile.read(2))[0]
            encrypted_aes_key = infile.read(encrypted_key_length)

            aes_key = private_key.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

            aesgcm = AESGCM(aes_key)

            output_path = Path(output_folder) / original_name

            with open(output_path, "wb") as outfile:
                chunk_index = 0

                while True:
                    nonce = infile.read(NONCE_SIZE)
                    if not nonce:
                        break

                    size_data = infile.read(4)
                    if len(size_data) != 4:
                        raise HybridError("Corrupted hybrid package.")

                    encrypted_chunk_size = struct.unpack(">I", size_data)[0]
                    encrypted_chunk = infile.read(encrypted_chunk_size)

                    if len(encrypted_chunk) != encrypted_chunk_size:
                        raise HybridError("Corrupted hybrid package.")

                    aad = MAGIC + original_name_bytes + struct.pack(">Q", chunk_index)

                    try:
                        decrypted_chunk = aesgcm.decrypt(nonce, encrypted_chunk, aad)
                    except InvalidTag:
                        raise HybridError("Package was modified or corrupted.")

                    outfile.write(decrypted_chunk)
                    chunk_index += 1

        return str(output_path)

    except HybridError:
        raise
    except Exception as e:
        raise HybridError(f"Hybrid decryption failed: {e}")