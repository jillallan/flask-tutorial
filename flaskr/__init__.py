import os

from flask import Flask


def create_app(test_config=None):
    '''Create a flask instance, set up configuration, registration and a database

    test_config -- test config settings
    '''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # create the instance folder to store the SQLite database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # call the init_app to register the included functions with the app
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
