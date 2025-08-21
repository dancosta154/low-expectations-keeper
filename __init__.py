
from __future__ import annotations
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev-secret-key"),
        LEAGUE_ID=os.environ.get("LEAGUE_ID"),
        ESPN_SWID=os.environ.get("ESPN_SWID"),
        ESPN_S2=os.environ.get("ESPN_S2"),
        LAST_SEASON=int(os.environ.get("LAST_SEASON", "2024")),
    )

    missing = [k for k in ("LEAGUE_ID", "ESPN_SWID", "ESPN_S2") if not app.config.get(k)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    return app
