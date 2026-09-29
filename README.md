# 💼 Job Application Tracker

A secure, full-stack web application built to help job seekers log, manage, and monitor their active employment applications in real-time. This project features a hybrid architecture combining server-rendered views with an internal asynchronous **RESTful API backend**.

---

## ✨ Features

- **User Authentication:** Secure registration, login, and logout state tracking using session-cookies (`Flask-Login`) and safely encrypted password storage (`Flask-Bcrypt`).
- **Full CRUD Support:** Add new job applications, dynamically update application status metrics via the client dashboard, and delete accidental entries.
- **RESTful API Layer:** Modular endpoint architecture returning clean JSON payloads (`/api/jobs`) decoupled from standard web views.
- **Seamless UI Updates:** Driven asynchronously by modern client-side vanilla JavaScript (`fetch()`), eliminating explicit full-page browser refreshes.
- **Database Migrations:** Robust database schema tracking using `Flask-Migrate` (Alembic) to scale database columns seamlessly without discarding data rows.
- **Automated Testing Suite:** Implements structured unit tests covering isolation states, authentication checks, and database assertions via `pytest`.

---

## 🛠️ Technology Stack

- **Backend Framework:** Python 3, Flask
- **Database ORM:** SQLite, Flask-SQLAlchemy
- **Validation & Forms:** Flask-WTF, WTForms
- **Styling:** Custom Vanilla CSS3 (Responsive Grid/Flexbox Layouts)
- **Testing Engine:** Pytest

---

## 📁 Project Architecture

```text
job_tracker/
│
├── app/
│   ├── __init__.py          # App Factory Initialization & Extension Binding
│   ├── models.py            # Relational SQLAlchemy Database Schemas
│   │
│   ├── auth/                # Authentication Blueprint (Forms & Session Views)
│   ├── main/                # Main Blueprint (Core Dashboard Controller)
│   ├── api/                 # RESTful API Blueprint (JSON Endpoints)
│   │
│   ├── static/              # Asset Pipeline (Custom Custom style.css)
│   └── templates/           # Shared UI Layout Frameworks (base.html, index.html)
│
├── tests/                   # Automated Pytest Suite Engine (test_app.py)
├── migrations/              # Database Upgrade Schema Tracking Scripts
├── .env.example             # Safe Architecture Credential Template Blueprint
├── requirements.txt         # Production Production Cloud Engine Dependency List
└── run.py                   # Local Project Script Entrypoint
```

---

## 🚀 Local Installation & Setup

Follow these steps to run the application locally on your computer:

### 1. Clone the Project Workspace
```bash
git clone https://github.com
cd job-application-tracker
```

### 2. Configure Virtual Environment & Dependencies
```bash
# Create and activate environment setup
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install exact environment property dependencies
pip install -r requirements.txt
```

### 3. Establish Local Environment Properties
Duplicate the repository blueprint template file to configure your local secret parameters:
```bash
cp .env.example .env
```
Open your newly created `.env` file and generate a custom values string for your `SECRET_KEY`.

### 4. Build Database Schema Migrations
```bash
flask db init
flask db migrate -m "Initial schema tracking configuration"
flask db upgrade
```

### 5. Fire Up the Server Engine
```bash
python run.py
```
Open your browser and navigate to **`http://127.0.0`** to register an account and start tracking your applications.

---

## 🧪 Running Automated Tests

Verify that your application components are completely secure and function properly by invoking the test engine runner:
```bash
pytest
```

---

## 📡 Core API Reference Endpoints

| Method | Endpoint | Description | Payload Example |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/jobs` | Retrieve list entries for all tracked jobs. | `None` |
| **POST** | `/api/jobs` | Create and bind a new application row. | `{"company": "Google", "role": "Engineer", "user_id": 1}` |
| **DELETE** | `/api/jobs/<id>` | Erase a specific application row. | `None` |

