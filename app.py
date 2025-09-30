from flask import Flask, render_template, request, jsonify, redirect, url_for, g
import sqlite3
from blog import blog_bp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ================= EXO 9: SQLite =================
def get_db():
    """Retourne la connexion SQLite actuelle (ou en crée une)"""
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Ferme la connexion SQLite après chaque requête"""
    db_conn = g.pop('db', None)
    if db_conn is not None:
        db_conn.close()

def init_sqlite():
    """Initialise la table users si elle n'existe pas"""
    db_conn = get_db()
    db_conn.execute("CREATE TABLE IF NOT EXISTS users(name TEXT)")
    db_conn.commit()

# ================= EXO 14: SQLAlchemy Model =================
class Note(db.Model):
    """Modèle SQLAlchemy pour les notes (title, body)"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)

# ================= EXERCICES 1 à 15 =================

# EXO 1: /hello
@app.route('/hello')
def hello():
    return "Hello World"

# EXO 2: /contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# EXO 3: /user/<name>
@app.route('/user/<name>')
def user(name):
    return f"Bonjour {name} !"

# EXO 4: index.html extends base.html
@app.route('/')
def index():
    return render_template('index.html')

# EXO 5: /age form (GET/POST)
@app.route('/age', methods=['GET', 'POST'])
def age():
    age_val = None
    if request.method == 'POST':
        age_val = request.form.get('age')
    return render_template('age.html', age=age_val)

# EXO 6: affichage d'une liste d'articles dans un template
articles = [
    {"title": "Article 1", "author": "Alice"},
    {"title": "Article 2", "author": "Bob"},
]
@app.route('/articles')
def articles_view():
    return render_template('articles.html', articles=articles)

# EXO 8: /api/ping JSON
@app.route('/api/ping')
def api_ping():
    return jsonify({"ping": "pong"})

# EXO 9: ajout d'utilisateur dans SQLite
@app.route('/add_user/<name>')
def add_user(name):
    db_conn = get_db()
    db_conn.execute("INSERT INTO users(name) VALUES(?)", (name,))
    db_conn.commit()
    return f"Utilisateur {name} ajouté"

# EXO 10: liste des utilisateurs depuis SQLite
@app.route('/users')
def list_users():
    db_conn = get_db()
    users = db_conn.execute("SELECT * FROM users").fetchall()
    return render_template('users.html', users=users)

# EXO 11: gestionnaire d'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# EXO 12: query string /search?q=...
@app.route('/search')
def search():
    q = request.args.get('q')
    return f"Vous avez recherché : {q}"

# EXO 13: Blueprint blog
app.register_blueprint(blog_bp, url_prefix='/blog')

# EXO 14: routes pour SQLAlchemy (notes)
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

# EXO 15: /api/patients renvoie JSON depuis SQLite
@app.route('/api/patients')
def api_patients():
    db_conn = get_db()
    patients = db_conn.execute("SELECT * FROM users").fetchall()
    return jsonify([dict(p) for p in patients])

# ================= MAIN =================
if __name__ == '__main__':
    with app.app_context():
        # EXO 9: Initialisation SQLite
        init_sqlite()
        
        # EXO 14: Initialisation SQLAlchemy
        db.create_all()

        # ======= Initialisation automatique des données =======
        # Ajouter quelques utilisateurs si la table est vide
        db_conn = get_db()
        existing_users = db_conn.execute("SELECT * FROM users").fetchall()
        if not existing_users:
            users_to_add = ['Alice', 'Bob', 'Charlie']
            for u in users_to_add:
                db_conn.execute("INSERT INTO users(name) VALUES(?)", (u,))
            db_conn.commit()
            print("Utilisateurs initiaux ajoutés : Alice, Bob, Charlie")

        # Ajouter quelques notes si la table est vide
        existing_notes = Note.query.all()
        if not existing_notes:
            notes_to_add = [
                Note(title="Note 1", body="Contenu de la note 1"),
                Note(title="Note 2", body="Contenu de la note 2"),
            ]
            for n in notes_to_add:
                db.session.add(n)
            db.session.commit()
            print("Notes initiales ajoutées : Note 1, Note 2")

    app.run(debug=True)
