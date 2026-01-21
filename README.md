# 🐍 Python-System-Automation-with-MD5
### Intelligent Storage Cleanup & Automated Audit System

This repository features a production-ready automation script designed to maintain system storage integrity by identifying and removing duplicate files. The system is built for accuracy and includes a remote monitoring feature via automated email logging.

---

## 🚀 Key Features

- **MD5 Checksum Verification:** Unlike basic filename comparisons, this system uses `hashlib` to generate unique MD5 signatures for every file, ensuring 100% accuracy in detecting duplicates even if they are renamed.
- **Periodic Execution:** Integrated with the `schedule` library to perform automated directory scans at predefined intervals.
- **Automated Audit Logs:** Generates a detailed, timestamped log file of every operation performed (detection, deletion, and errors).
- **Remote Email Alerts:** Utilizes `smtplib` to automatically share execution logs via email, allowing for remote oversight of system maintenance.

---

## 🛠️ Tech Stack & Skills
- **Language:** Python
- **Core Modules:** `os` (File manipulation), `hashlib` (Data integrity), `shutil` (System operations)
- **Automation Tools:** `schedule` for task orchestration
- **Networking:** `smtplib` for email automation
- **Programming Paradigm:** Object-Oriented Programming (OOP)

---

## 📂 Project Structure
```text
├── src/
│   └── main_automation.py   # Core logic for scanning and deletion
├── logs/
│   └── execution_log.txt    # Automatically generated operation audits
├── requirements.txt         # Dependencies for the project
└── README.md                # Project documentation


## 🛠️ Installation & Setup Guide

Follow these steps to deploy the automation system on your local machine.

 1. Clone the Repository
```bash
git clone [https://github.com/Bhavesh112004/Python-System-Automation-with-MD5.git](https://github.com/Bhavesh112004/Python-System-Automation-with-MD5.git)
cd Python-System-Automation-with-MD5

2. Configure Virtual Environment

python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Run the Automation

python src/main_automation.py


