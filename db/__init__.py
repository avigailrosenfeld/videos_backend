from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

db = SQLAlchemy()
meta = MetaData()


def initialize_db(app):
    app.logger.info("Initializing mySql")
    db.init_app(app)
    try:
        if 'test' in app.config.get('SQLALCHEMY_DATABASE_URI'):
            with app.app_context():
                db.engine.execute("DROP TABLE users;")
    except Exception as e:
        pass
