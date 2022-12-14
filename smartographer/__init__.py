from smartographer.maps import get_tag_list

from flask import Flask, render_template

import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(
            app.instance_path, 'smartographer.sqlite'
            ),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        tag_list = get_tag_list(is_map=False)
        return render_template('index.html', tag_list=tag_list)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import maps
    app.register_blueprint(maps.bp)

    return app
