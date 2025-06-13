from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("SECRET_KEY", "super-secret-dev-key")

    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'data', 'uploaded_emails')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    from app import routes
    app.register_blueprint(routes.bp)

    return app
