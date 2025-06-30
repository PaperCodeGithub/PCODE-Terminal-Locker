# 🔐 PCODE Terminal System Locker

A Python-based, terminal-only system locker simulation — featuring USB authentication, 2FA email verification, keyboard lockdown, and encrypted credentials. Built entirely in terminal/CUI style for educational and ethical red-team scenarios.

> ⚠️ For educational purposes only. Do not deploy on critical machines.

---

## 🚀 Features

- 🔐 Terminal fullscreen system lock
- 🔑 USB verification based on drive serial
- 📧 Email 2FA verification with 4-digit unlock code
- ⌨️ Full keyboard input lockdown (via `keyboard` module)
- 🧬 Custom launcher to auto-start system based on setup state
- 🧠 Built 100% in Python — no external GUI frameworks

---

## 📁 File Structure
```
PCODE-System-Locker/
├── launcher.py # Entry point; detects first-time use
├── Bin/
    ├── setup.py # User setup for email, unlock code, and USB registration
    ├── lock.py # Lockdown logic, keyboard block, 2FA challenge
├── config 
    ├── .env.example # Template for environment secrets
    ├── config.json # Auto-generated config file
└── README.md # You're here.

```

## ⚙️ Requirements

- Python 3.8+
Required:
- `python-dotenv`
- `smtplib`
- `keyboard`
- `colorama`

---

## 📧 Setting Up Email for 2FA

To enable email verification, create a `.env` file in the bin directory:

```env
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_PASSWORD=your_app_password
```
⚠️ Use a Gmail App Password — not your real password
Generate it at https://myaccount.google.com/apppasswords (after enabling 2-Step Verification)

## 🧪 How to Run
- Clone the repo
- Create .env with your email and app password
- Launch the system:
- `bash`
- `Copy`
- `Edit`
- python launcher.py
- On first run: launches setup.py for config
- On next runs: locks system via locker.py

## 🔐 How It Works
1. First-Time Setup
  - Collects email & unlock code
  - Registers the USB key
  - On Launch
  - Waits for correct USB + unlock code
  - Sends verification email
  - Upon confirmation, unlocks terminal

2. Failsafes
- Emergency hotkey (optional for devs)
- Lock screen prevents input via keyboard.block_key()

## 📜 License
This project is licensed under the MIT License.
Use it freely, but you are responsible for any misuse or data loss.

## 👨‍💻 Author
Built with obsession by PaperCode 🧠

## 💬 Want to Contribute?
- Fork and star the repo ✨
- Suggest features (GUI version? Email log? Encryption upgrade?)
- Share the project with friends learning security
