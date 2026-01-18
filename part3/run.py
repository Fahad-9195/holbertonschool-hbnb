import os
from dotenv import load_dotenv
from app import create_app
from config import DevelopmentConfig, ProductionConfig, TestingConfig

load_dotenv()

# Map FLASK_ENV to config class
env = os.getenv('FLASK_ENV', 'development')
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
config_class = config_map.get(env, DevelopmentConfig)

app = create_app(config_class)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
