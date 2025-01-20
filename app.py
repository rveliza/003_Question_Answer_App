from flask import Flask, render_template, g, request
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True

def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('home.html')


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

        return f"Password: {hashed_password}"
    return render_template('register.html')


@app.route('/login')
def login():
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

if __name__ == "__main__":
    app.run()