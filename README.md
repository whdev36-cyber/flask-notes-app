# Flask Notes App 📝

This is a minimal note-taking web application built with **Flask**, styled using **[Pico.css](https://picocss.com/)**. It supports user **authentication** and basic **CRUD (create only)** functionality for notes.

## 🚀 Features

- ✅ User Registration  
- ✅ User Login / Logout  
- ✅ Authenticated Notes Creation  
- ✅ Flash messages for feedback  
- ✅ Clean, responsive UI with Pico.css  

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Pico.css (Lightweight CSS framework)
- **Database**: SQLite (via SQLAlchemy ORM)
- **Form Handling**: Flask-WTF

## 📁 Routes Overview

### 🔐 Auth Blueprint (`/auth`)
| Route          | Methods       | Description          |
|----------------|---------------|----------------------|
| `/login`       | GET, POST     | Log into an account  |
| `/register`    | GET, POST     | Create a new account |
| `/logout`      | GET           | Logout from session  |

### 📄 Views Blueprint (`/`)
| Route     | Methods       | Description                 |
|-----------|---------------|-----------------------------|
| `/`       | GET, POST     | Home page + Note creation   |

## 🧪 Forms

### Register Form
- `name` — User’s full name
- `email` — Email (must be unique)
- `password` — Password (min 8 chars)
- `password_confirm` — Must match password

### Login Form
- `email`
- `password`
- `remember` (optional checkbox)

### Note Form
- `data` — Text area to write notes

## 📸 UI

The project uses [Pico.css](https://picocss.com/) for a minimal and clean design. No custom JavaScript is used — fully functional with HTML & Python backend.

## ▶️ Getting Started

```bash
# Clone the repository
git clone https://github.com/whdev36-cyber/flask-notes-app
cd flask-notes-app

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment variables
touch .env
# Add this to .env file:
# SECRET_KEY=your-secret-key

# Run the app
python -m website
````

## 📂 Project Structure

```
flask-notes-app/
│
├── website/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── auth.py
│   ├── views.py
│   ├── models.py
│   └── forms.py
├── .env
├── requirements.txt
└── README.md
```

## 📄 License

MIT License — Feel free to use, modify, and distribute this project.

---

Created with ❤️ by [whdev36-cyber](https://github.com/whdev36-cyber)

