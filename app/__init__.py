from flask import Flask
from app.db.connection import init_db

def create_app():
    app = Flask(__name__)
    init_db() 
    from app import routes
    app.register_blueprint(routes.bp)

    return app
