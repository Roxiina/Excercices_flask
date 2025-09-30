from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from blog import blog  # Ton blueprint

# Création de l'application Flask
app = Flask(__name__)

# Enregistrement du blueprint
app.register_blueprint(blog)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Modèle SQLAlchemy pour l'exercice 14
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)

# Exercice 1 : /hello
@app.route('/hello')
def hello():
    return "Hello World"

# Exercice 2 : /contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Exercice 3 : /user/<name>
@app.route('/user/<name>')
def user(name):
    return f"Bonjour {name} !"

# Exercice 4 : index avec base.html
@app.route('/')
def index():
    return render_template('index.html')

# Exercice 5 : formulaire /age
@app.route('/age', methods=['GET', 'POST'])
def age():
    age_value = None
    if request.method == 'POST':
        age_value = request.form.get('age')
    return render_template('age.html', age=age_value)

# Exercice 6 : liste d'articles
@app.route('/articles')
def show_articles():
    articles = [
        {"title": "Flask pour débutants", "author": "Alice"},
        {"title": "SQLAlchemy 101", "author": "Bob"}
    ]
    return render_template('articles.html', articles=articles)

# Exercice 7 : style.css est utilisé via base.html

# Exercice 8 : API ping
@app.route('/api/ping')
def api_ping():
    return jsonify({"ping": "pong"})

# Exercice 9 : SQLite pour table users
# Route pour ajouter un utilisateur
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            message = f"L'utilisateur {name} a été ajouté !"
        else:
            message = "Veuillez entrer un nom."
    return render_template('add_user.html', message=message)

# Route pour lister les utilisateurs
@app.route('/users')
def list_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

# Exercice 10 : lister les users
@app.route('/users')
def list_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT name FROM users')
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('users.html', users=users)

# Exercice 11 : 404 personnalisé
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Exercice 12 : query string /search?q=...
@app.route('/search')
def search():
    query = request.args.get('q')
    return f"Vous avez recherché : {query}"

# Exercice 14 : routes pour Notes
@app.route('/notes')
def list_notes():
    notes = Note.query.all()
    return "<br>".join([f"{n.title}: {n.body}" for n in notes])

@app.route('/notes/add', methods=['POST'])
def add_note():
    title = request.form.get('title')
    body = request.form.get('body')
    if title and body:
        note = Note(title=title, body=body)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('list_notes'))
    return "Erreur : titre et body requis"

# Exercice 15 : API patients (exemple SQLite)
@app.route('/api/patients')
def api_patients():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS patients (name TEXT)')
    c.execute('SELECT name FROM patients')
    patients = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify({"patients": patients})

if __name__ == '__main__':
    app.run(debug=True)
