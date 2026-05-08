from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pickle
import os

app = Flask(__name__)
app.secret_key = "diabetes_app_secret_123"

login_manager = LoginManager(app)
login_manager.login_view = "login"

# On Vercel the app directory is read-only; /tmp is the only writable location
DB_PATH = "/tmp/users.db" if os.environ.get("VERCEL") else os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT id, username, email FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm = request.form["confirm"]
        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")
        hashed = generate_password_hash(password)
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed))
            conn.commit()
            conn.close()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute("SELECT id, username, email, password FROM users WHERE username=?", (username,)).fetchone()
        conn.close()
        if row and check_password_hash(row[3], password):
            user = User(row[0], row[1], row[2])
            login_user(user)
            return redirect(url_for("home"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    result = None
    if request.method == "POST":
        model_path = os.path.join(os.path.dirname(__file__), "db.model")
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        fs = float(request.form["fs"])
        fu = request.form["fu"]
        d = [[fs, 0, 1]] if fu == "yes" else [[fs, 1, 0]]
        result = model.predict(d)[0]
    return render_template("home.html", m=result)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
