from flask import Flask, render_template, g, request, session, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)

def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    user = None
    if 'user' in session:
        user = session['user']

    return render_template('home.html', user=user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_db()

        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        db.execute("INSERT INTO users (name, password, expert, admin) VALUES (?,?,?,?)", [name, hashed_password, 0, 0])
        db.commit()
        return "User Created!"

    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()

        name = request.form['name']
        password = request.form['password']

        user_cur = db.execute("SELECT name, password FROM users WHERE name = ?", [name])
        user_result = user_cur.fetchone()

        same_password = check_password_hash(user_result['password'], password)
        if same_password:
            session['user'] = user_result['name'] 
            #Session: <SecureCookieSession {'user': 'admin'}>
            return "Password correct"
        else:
            return "Password incorrect"
    
    return render_template('login.html')


@app.route('/question')
def question():
    return render_template('question.html')


@app.route('/answer')
def answer():
    return render_template('answer.html')


@app.route('/ask')
def ask():
    return render_template('ask.html')


@app.route('/unanswered')
def unanswered():
    return render_template('unanswered.html')


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()