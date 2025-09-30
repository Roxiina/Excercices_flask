from flask import Blueprint

blog_bp = Blueprint('blog', __name__, template_folder='templates')

@blog_bp.route('/')
def blog_index():
    return "<h1>Bienvenue sur le blog !</h1>"
