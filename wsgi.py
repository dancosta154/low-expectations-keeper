import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

# Import Flask and create app directly
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Create Flask app with correct template and static directories
app = Flask(__name__, 
           template_folder='app/templates',
           static_folder='app/static')

# Configure app
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev-secret-key"),
    LEAGUE_ID=os.environ.get("LEAGUE_ID"),
    ESPN_SWID=os.environ.get("ESPN_SWID"),
    ESPN_S2=os.environ.get("ESPN_S2"),
    LAST_SEASON=int(os.environ.get("LAST_SEASON", "2024")),
    COMMISSIONER_EMAIL=os.environ.get("COMMISSIONER_EMAIL", ""),
)

# Import and register blueprint
try:
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
except ImportError:
    # Fallback: create a simple route
    @app.route("/")
    def index():
        return "Keeper App - Import Error. Check logs."

if __name__ == "__main__":
    app.run()
