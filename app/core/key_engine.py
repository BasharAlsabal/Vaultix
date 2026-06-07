from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class KeyEngineError(Exception):
    pass


def generate_rsa_key_pair(
    output_folder: str,
    private_password: str,
) -> tuple[str, str]:
    if not private_password or len(private_password) < 8:
        raise KeyEngineError("Private key password must be at least 8 characters.")

    folder = Path(output_folder)

    if not folder.exists() or not folder.is_dir():
        raise KeyEngineError("Output folder does not exist.")

    private_key_path = folder / "vaultix_private_key.pem"
    public_key_path = folder / "vaultix_public_key.pem"

    if private_key_path.exists() or public_key_path.exists():
        raise KeyEngineError("Key files already exist in this folder.")

    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )

        encrypted_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                private_password.encode("utf-8")
            ),
        )

        public_key = private_key.public_key()

        public_key_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        private_key_path.write_bytes(encrypted_private_key)
        public_key_path.write_bytes(public_key_data)

        return str(private_key_path), str(public_key_path)

    except Exception as e:
        raise KeyEngineError(f"Failed to generate keys: {e}")