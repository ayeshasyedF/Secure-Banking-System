# Secure Banking System

> Built with a focus on security-first design, not just functionality.

This project implements a secure client–server banking system that simulates an ATM interface communicating with a backend server. The system supports authentication and financial transactions while ensuring that all communication is encrypted, verified, and protected against tampering.

The focus of this project is not just functionality, but building a system where trust is established, data is secured, and every transaction is handled safely.

## 🚀 Features

* Secure client–server architecture using sockets
* Graphical ATM interface
* Authenticated key exchange protocol
* AES encryption for secure communication
* Message Authentication Code (MAC) for integrity
* Key derivation for encryption and MAC keys
* Transaction support for deposit, withdraw, and balance
* Audit logging of all activity

## 🏗️ Project Structure

```
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
```

## ⚙️ How to Run

### 1. Install Dependencies

Make sure Python is installed, then run:

```bash
pip install -r requirements.txt
```

---

### 2. Start the Server

Run the backend server:

```bash
python -m backend.server
```

You should see output such as:

* Server started
* Client connected
* Authentication success
* Transactions processed

Leave this running.

---

## 🖥️ Running the GUI (Client)

The graphical ATM interface acts as the client and communicates with the backend server over a socket connection.

### Step 1: Launch the GUI

Open a new terminal and run:

```bash
python -m frontend.gui
```

This will open the ATM interface.

---

### Step 2: Log In

Use a valid username from:

```
data/database.json
```

After login, the dashboard will appear.

---

### Step 3: Perform Transactions

Using the GUI, you can:

* Deposit funds
* Check balance
* View transaction history

Each action:

* Is sent to the server
* Is encrypted using AES
* Includes a MAC for integrity
* Is processed securely by the backend
* Updates the audit log

---

### ⚠️ Important Notes

* The server must be running before the GUI
* Run commands from the project root directory
* If the GUI does not open, run locally (Tkinter requires a display)

---

### 💡 Key Insight

The GUI does not execute banking logic locally.
All actions are securely sent to the backend server, which handles authentication, transaction processing, and logging.

## 🔐 Security Design

This system enforces multiple layers of security:

* **Authentication**
  Users must be verified before accessing the system

* **Key Exchange**
  A shared master secret is established securely

* **Key Derivation**
  Two keys are derived:

  * Encryption key for confidentiality
  * MAC key for integrity

* **Encryption (AES)**
  All transaction data is encrypted before transmission

* **Message Authentication Code (MAC)**
  Ensures data is not altered in transit

* **Audit Logging**
  All transactions are recorded in `logs/audit_log.txt`

## 📸 Showcase

* Secure login and dashboard interface
* Encrypted transaction processing
* Real-time transaction receipts
* Audit logging system

> All transactions are encrypted and authenticated before being processed.

## 🔄 Example Flow

Client → Server
→ Authentication
→ Key Exchange
→ Shared Secret Established
→ Keys Derived
→ Encrypted Transaction Sent
→ MAC Verified
→ Transaction Processed
→ Log Updated

## 📝 Notes

* The server must be running before the client
* Multiple clients can connect simultaneously
* User data is stored locally in JSON format
* Logs are updated after every transaction
* All communication is encrypted and authenticated

## 🔮 Future Improvements

* Add user registration
* Replace JSON with a database such as SQL
* Expand transaction features
* Add multi-factor authentication
* Deploy over a real network
