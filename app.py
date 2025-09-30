from flask import Flask, render_template, request, jsonify, redirect, url_for, g
import sqlite3
from blog import blog_bp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ========== SQLite setup =========
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_sqlite():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users(name TEXT)")
    db.commit()

init_sqlite()

# ========= SQLAlchemy Model =========
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)

db.create_all()

# ========= Routes =========
@app.route('/hello')
def hello():
    return "Hello World"

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user/<name>')
def user(name):
    return f"Bonjour {name} !"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/age', methods=['GET', 'POST'])
def age():
    age = None
    if request.method == 'POST':
        age = request.form.get('age')
    return render_template('age.html', age=age)

articles = [
    {"title": "Article 1", "author": "Alice"},
    {"title": "Article 2", "author": "Bob"},
]
@app.route('/articles')
def articles_view():
    return render_template('articles.html', articles=articles)

@app.route('/api/ping')
def api_ping():
    return jsonify({"ping": "pong"})

@app.route('/add_user/<name>')
def add_user(name):
    db = get_db()
    db.execute("INSERT INTO users(name) VALUES(?)", (name,))
    db.commit()
    return f"Utilisateur {name} ajouté"

@app.route('/users')
def list_users():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template('users.html', users=users)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/search')
def search():
    q = request.args.get('q')
    return f"Vous avez recherché : {q}"

# Blueprint blog
app.register_blueprint(blog_bp, url_prefix='/blog')

# Notes routes
@app.route('/notes')
def list_notes():
    notes = Note.query.all()
    return render_template('articles.html', articles=notes)

@app.route('/notes/create', methods=['POST'])
def create_note():
    title = request.form.get('title')
    body = request.form.get('body')
    note = Note(title=title, body=body)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for('list_notes'))

@app.route('/api/patients')
def api_patients():
    db = get_db()
    patients = db.execute("SELECT * FROM users").fetchall()
    return jsonify([dict(p) for p in patients])

if __name__ == '__main__':
    app.run(debug=True)
