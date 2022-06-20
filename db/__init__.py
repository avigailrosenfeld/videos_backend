from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_db(app):
    app.logger.info("Initializing mySql")
    db.init_app(app)
