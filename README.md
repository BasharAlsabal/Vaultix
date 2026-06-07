# Vaultix

**Vaultix — Offline Secure Sharing & Encryption Suite**

© 2026 Bashar Alsabal. All rights reserved.

---

## Overview

Vaultix is a professional offline desktop cybersecurity application developed in Python using PySide6.

The application enables users to encrypt, decrypt, protect, verify, hide, sign, and securely share sensitive information without relying on cloud services or internet connectivity.

All cryptographic operations are performed locally on the user's device, ensuring maximum privacy and security.

---

## Key Features

### File & Folder Protection

- AES-256-GCM file encryption
- AES-256-GCM folder encryption
- Password-based encryption
- Large file support

### Public Key Cryptography

- RSA-4096 key generation
- Public/private key secure sharing
- Hybrid AES + RSA encryption

### Digital Signatures

- File signing using RSA
- Signature verification
- Authenticity validation

### Integrity Verification

- SHA-256 hash generation
- File integrity checking
- Tampering detection

### Steganography

- Hide encrypted data inside PNG images
- Extract hidden data from PNG images

### Secure Deletion

- Multi-pass file shredding
- Permanent secure deletion

### Audit Logging

- SQLite-based history database
- Security operation tracking
- Dashboard statistics

---

## Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| GUI Framework | PySide6 (Qt) |
| Database | SQLite |
| Cryptography | cryptography |
| Image Processing | Pillow |
| Packaging | PyInstaller |

---

## Security Architecture

Vaultix combines modern cryptographic techniques to provide secure offline protection:

- AES-256-GCM for data encryption
- RSA-4096 for key exchange
- SHA-256 for integrity verification
- Digital signatures for authenticity
- Secure file shredding for permanent deletion

All operations are performed locally and no data is transmitted to external servers.

---

# Application Screenshots

## Dashboard

Main control center displaying security modules and application status.

![Dashboard](screenshots/screenshotsdashboard.png)

---

## Encrypt File

Encrypt files using AES-256-GCM password-based encryption.

![Encrypt File](screenshots/screenshotsencrypt_file.png)

---

## Decrypt File

Restore encrypted files using the correct password.

![Decrypt File](screenshots/screenshotsdecrypt_file.png)

---

## Generate RSA Keys

Generate RSA-4096 public/private key pairs for secure sharing.

![Generate Keys](screenshots/screenshotsgenerate_keys.png)

---

## Digital Signatures

Create digital signatures to prove file authenticity.

![Sign File](screenshots/screenshotssign_file.png)

---

## Verify Signatures

Verify signed files using public keys.

![Verify Signature](screenshots/screenshotsverify_signature.png)

---

## Steganography

Hide protected information inside PNG images.

![Hide Data](screenshots/screenshotshide_data.png)

---

## Audit Logs

Track all important security operations locally.

![History](screenshots/screenshotshistory.png)

---

## Secure Delete

Permanently destroy files using overwrite passes.

![Secure Delete](screenshots/screenshotssecure_delete.png)

---

## About Vaultix

Application information and security specifications.

![About](screenshots/screenshotsabout.png)

---

## Project Structure

```text
Vaultix/
├── app/
├── screenshots/
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## Author

**Bashar Alsabal**

Information Security Graduate  
Cybersecurity & Software Development Enthusiast

---

## License

MIT License