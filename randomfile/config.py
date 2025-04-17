import os
from pathlib import Path

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    BASE_PATH = Path(os.environ.get('BASE_PATH') or 'data/').resolve()
    
    @staticmethod
    def init_app(app):
        """Initialize the application with this configuration."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    
class ProductionConfig(Config):
    """Production configuration."""
    # Production-specific settings
    pass

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}