from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    with app.app_context():
        # Register user controller
        from app.controller.user_controller import user_bp
        app.register_blueprint(user_bp)

        # Register dailytime controller
        from app.controller.dailytime_controller import dailytime_bp
        app.register_blueprint(dailytime_bp)

        # Register monthtime controller
        from app.controller.monthtime_controller import monthtime_bp
        app.register_blueprint(monthtime_bp)

        # Register triviaquestion controller
        from app.controller.triviaquestion_controller import triviaquestion_bp
        app.register_blueprint(triviaquestion_bp)

        # Register accomplishment controller
        from app.controller.accomplishment_controller import accomplishment_bp
        app.register_blueprint(accomplishment_bp)

        # Register achievement controller
        from app.controller.achievement_controller import achievement_bp
        app.register_blueprint(achievement_bp)

        # Register dailytoken controller
        from app.controller.dailytoken_controller import dailytoken_bp
        app.register_blueprint(dailytoken_bp)

        # Register streak controller
        from app.controller.streak_controller import streak_bp
        app.register_blueprint(streak_bp)

        # Register rogue boss user controller
        from app.controller.rbuser_controller import rbuser_bp
        app.register_blueprint(rbuser_bp)

        # Register todo controller
        from app.controller.todo_controller import todo_bp
        app.register_blueprint(todo_bp)

        # Register kanban controller
        from app.controller.kanban_controller import kanban_bp
        app.register_blueprint(kanban_bp)

        # Register reminder controller
        from app.controller.reminder_controller import reminder_bp
        app.register_blueprint(reminder_bp)
    
    return app
