from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///test.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    try:
        from .routes import main
        app.register_blueprint(main)
    except Exception:
        pass

    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app