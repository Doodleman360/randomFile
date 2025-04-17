import os
from randomfile import create_app

# Get configuration from the environment or use default
config_name = os.environ.get('FLASK_CONFIG') or 'default'

# Create the application
app = create_app(config_name)

if __name__ == "__main__":
    app.run(debug=True)