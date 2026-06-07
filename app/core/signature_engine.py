from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


CHUNK_SIZE = 1024 * 1024 * 4


class SignatureError(Exception):
    pass


def load_private_key(private_key_path: str, password: str):
    path = Path(private_key_path)

    if not path.exists() or not path.is_file():
        raise SignatureError("Private key file does not exist.")

    try:
        return serialization.load_pem_private_key(
            path.read_bytes(),
            password=password.encode("utf-8"),
        )
    except Exception:
        raise SignatureError("Failed to load private key. Check password or key file.")


def load_public_key(public_key_path: str):
    path = Path(public_key_path)

    if not path.exists() or not path.is_file():
        raise SignatureError("Public key file does not exist.")

    try:
        return serialization.load_pem_public_key(path.read_bytes())
    except Exception:
        raise SignatureError("Failed to load public key.")


def hash_file(file_path: str) -> bytes:
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise SignatureError("File does not exist.")

    digest = hashes.Hash(hashes.SHA256())

    with open(path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)

    return digest.finalize()


def sign_file(file_path: str, private_key_path: str, password: str, output_path: str) -> str:
    private_key = load_private_key(private_key_path, password)
    file_digest = hash_file(file_path)

    try:
        signature = private_key.sign(
            file_digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        Path(output_path).write_bytes(signature)
        return output_path

    except Exception as e:
        raise SignatureError(f"Signing failed: {e}")


def verify_signature(file_path: str, public_key_path: str, signature_path: str) -> bool:
    public_key = load_public_key(public_key_path)
    file_digest = hash_file(file_path)

    sig_path = Path(signature_path)

    if not sig_path.exists() or not sig_path.is_file():
        raise SignatureError("Signature file does not exist.")

    signature = sig_path.read_bytes()

    try:
        public_key.verify(
            signature,
            file_digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True

    except InvalidSignature:
        return False

    except Exception as e:
        raise SignatureError(f"Verification failed: {e}")