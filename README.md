# 🤝 Decide-Mieux

**Decide-Mieux** is a simple, elegant platform for organizing collective decisions. Users can create polls, define choices, and invite others to evaluate them based on a shared scale.

This project is built using **Flask** (Python web framework) and **SQLite** for lightweight storage. It's ideal for small groups, teams, or workshops who want to make better shared decisions.

---

## 🌐 Live Demo

Once deployed, your app will be accessible at:

https://your-app-name.onrender.com


---

## 🧩 Features

- ✅ Create polls with multiple options and descriptions
- ✅ Assign a decision "scale" (e.g., important–neutral–irrelevant)
- ✅ Invite contributors to vote
- ✅ View results in real time
- ✅ Creator dashboard with private access
- ✅ Password protection for creators

---

## 📁 Project Structure

    decide-mieux/
    │
    ├── app/ # Core application (routes, models, templates)
    │ ├── templates/ # HTML templates (Bootstrap-based)
    │ ├── routes.py # All Flask routes
    │ ├── models.py # Database models
    │ └── init.py # App factory (optional)
    │
    ├── run.py # Entry point to launch the app
    ├── requirements.txt # Python dependencies
    ├── Procfile # Start command for deployment (gunicorn)
    └── README.md # This file


---

## 🚀 Deploy on Render

You can deploy this project for free using [Render](https://render.com/):

1. **Create a GitHub Repository** and push your project there.
2. Go to [https://render.com](https://render.com) and create a free account.
3. Click **“New Web Service”** → **“Deploy from GitHub.”**
4. Select your repo and fill in:
    - **Build Command**:  
      ```
      pip install -r requirements.txt
      ```
    - **Start Command**:  
      ```
      gunicorn run:app
      ```
5. Wait for it to deploy! Your app will be publicly accessible.

---

## 🔐 Creator Login Setup

Poll creators need to authenticate with a pseudonym and password.

To configure authorized creators, modify this dictionary in `routes.py`:

```python
CREATOR_CREDENTIALS = {
    "jean": "secure123",
    "alice": "mypassword"
}
```

You can later move this to a secure .env file or database.

## ✅ To Run Locally
Install dependencies:

    pip install -r requirements.txt
Run the app:

    python run.py

Open your browser at http://127.0.0.1:5000

## 📄 License
MIT License (or any other you prefer).

🧠 Acknowledgments
This app was designed for simplicity and meaningful collaboration. Built with love and logic.




