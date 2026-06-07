# Vaultix

**Vaultix — Offline Secure Sharing & Encryption Suite**

© 2026 Bashar Alsabal. All rights reserved.

---

## Overview

Vaultix is a professional offline desktop cybersecurity application built with Python and PySide6.

The application helps users encrypt, protect, hide, sign, verify, and securely share sensitive information before sending it through the internet.

Vaultix performs all cryptographic operations locally and does not require an internet connection.

---

## Features

### Encryption

- AES-256-GCM File Encryption
- AES-256-GCM Folder Encryption
- Password-Based Protection
- Large File Support

### Key Management

- RSA-4096 Key Generation
- Public / Private Key Sharing
- Hybrid Encryption (RSA + AES)

### Integrity & Verification

- SHA-256 Integrity Verification
- Digital Signatures
- Signature Verification

### Steganography

- Hide Files Inside PNG Images
- Extract Hidden Data From PNG Images

### Secure Deletion

- Multi-Pass File Shredding
- Secure Permanent Deletion

### Audit & Tracking

- SQLite Audit Logs
- Dashboard Statistics
- Operation History

---

## Technology Stack

- Python
- PySide6 (Qt)
- SQLite
- Cryptography
- Pillow
- PyInstaller

---

## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Encrypt File

![Encrypt File](screenshots/encrypt_file.png)

### Generate Keys

![Generate Keys](screenshots/generate_keys.png)

### Sign File

![Sign File](screenshots/sign_file.png)

### Hide Data

![Hide Data](screenshots/hide_data.png)

### History

![History](screenshots/history.png)

---

## Security Features

- AES-256-GCM Encryption
- RSA-4096 Public Key Cryptography
- SHA-256 Integrity Verification
- Digital Signatures
- Hybrid Secure Sharing
- Offline Operation
- Secure File Shredding

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

Cybersecurity & Information Security Graduate

---

## License

This project is licensed under the MIT License.