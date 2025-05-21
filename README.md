# 📝 Flask Notes App

A simple, modern Flask-based note-taking web app with user authentication, note CRUD operations, and Bootstrap 5 UI.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![License](https://img.shields.io/github/license/whdev36-cyber/flask-notes-app)
![Repo Size](https://img.shields.io/github/repo-size/whdev36-cyber/flask-notes-app)

---

## 🌐 Live Preview

> Coming soon! Or clone and run locally (see below).

---

## 📁 Project Structure

```

.
├── app.py                 # Main application file
├── data
│   └── notes.json         # Sample or backup notes data
├── LICENSE
├── README.md
├── requirements.txt       # Python dependencies
├── templates              # HTML templates using Jinja2
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── note_form.html
│   └── register.html
└── website.db             # SQLite database

````

---

## 🚀 Features

- ✅ User Registration & Login (Flask-Login, hashed passwords)
- ✅ Create, View, Edit & Delete personal notes
- ✅ SQLite database (via SQLAlchemy ORM)
- ✅ Bootstrap 5 UI with icons
- ✅ Flash messages for UX feedback
- ✅ Session handling with CSRF protection

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/whdev36-cyber/flask-notes-app.git
cd flask-notes-app
````

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Visit [http://localhost:5555](http://localhost:5555) in your browser.

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and set your secret key:

```env
SECRET_KEY=your-secret-key-here
```

---

## 🧪 Sample Data

You can add sample users and notes with a script. Ask the maintainer or check out the `seed.py` example in issues/discussions.

---

## 📸 Screenshots

> Coming soon...

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## 🙌 Credits

Built by [whdev36-cyber](https://github.com/whdev36-cyber) using Flask, SQLAlchemy, Flask-WTF, and Bootstrap 5.

---

## 🌟 Star the project

If you like this project, give it a ⭐ on [GitHub](https://github.com/whdev36-cyber/flask-notes-app)!

