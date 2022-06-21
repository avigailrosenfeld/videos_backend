from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask.wrappers import Response
import json

db = SQLAlchemy()
meta = MetaData()


def initialize_db(app):
    app.logger.info("Initializing mySql")
    db.init_app(app)
    # TODO move to tests
    try:
        if 'test' in app.config.get('SQLALCHEMY_DATABASE_URI'):
            with app.app_context():
                db.engine.execute("DROP TABLE users;")
    except Exception as e:
        return Response(json.dumps({'message': 'Register faild'}), mimetype="application/json", status=400)
