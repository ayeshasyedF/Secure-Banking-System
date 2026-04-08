
# Secure Banking System

> Built with a focus on security-first design, not just functionality.

This project implements a secure client–server banking system that simulates an ATM interface communicating with a backend server. The system supports authentication and financial transactions while ensuring that all communication is encrypted, verified, and protected against tampering.

The focus of this project is not just functionality, but building a system where trust is established, data is secured, and every transaction is handled safely.

## 🚀 Features

- Secure client–server architecture using sockets
- Graphical ATM interface
- Authenticated key exchange protocol
- AES encryption for secure communication
- Message Authentication Code (MAC) for integrity
- Key derivation for encryption and MAC keys
- Transaction support for deposit, withdraw, and balance
- Audit logging of all activity

## 🏗️ Project Structure

```text
Secure-Banking-System/
│
├── backend/
│   ├── server.py
│   ├── auth.py
│   ├── transaction.py
│   ├── database_handler.py
│   ├── audit.py
│   └── view_logs.py
│
├── crypto/
│   ├── aes_utils.py
│   ├── hmac_utils.py
│   ├── kdf_utils.py
│   ├── rsa_utils.py
│   └── crypto_utils.py
│
├── frontend/
│   ├── gui.py
│   ├── client.py
│   ├── theme.py
│   └── views/
│
├── data/
│   └── database.json
│
├── logs/
│   └── audit_log.txt
│
├── main.py
├── requirements.txt
└── README.md