import os
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.config import Config
from app.models import db, bcrypt

# Initialize extensions
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Ensure upload directories exist
    for directory in [app.config['UPLOAD_FOLDER'],
                     os.path.join(app.config['UPLOAD_FOLDER'], 'pcap'),
                     os.path.join(app.config['UPLOAD_FOLDER'], 'reports')]:
        os.makedirs(directory, exist_ok=True)

    # Import and register routes
    from app import routes

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

# Create application instance
app = create_app()

# Import models to ensure they are registered with SQLAlchemy
from app import models
