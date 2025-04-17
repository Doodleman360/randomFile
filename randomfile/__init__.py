from flask import Flask
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(config_name='default'):
    """
    Factory function to create and configure the Flask application.

    Args:
        config_name (str): The configuration to use (default, development, testing, production)

    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # Load configuration
    from randomfile.config import config
    app.config.from_object(config[config_name])

    # Configure logging
    if not app.debug:
        # Set up a file handler
        file_handler = logging.FileHandler('randomfile.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('RandomFile startup')

    # Configure security
    from randomfile.security import configure_security
    configure_security(app)

    # Initialize limiter
    limiter.init_app(app)

    # Register blueprints
    from randomfile.routes.main import main_bp
    from randomfile.routes.audio import audio_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(audio_bp)

    return app
