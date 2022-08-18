# Smartographer - A map making web application by James Maphis.
# Uses various algorithms to generate maps for all of your adventuring needs!
from mapmanager import MapManager
from auth import auth_bp

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape

app = Flask(__name__)
app.register_blueprint(auth_bp)
env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape(
        enabled_extensions = ('html', 'htm', 'xml'),
        disabled_extensions = (),
        default_for_string=True,
        default=False
    )
)

@app.route('/')
def index():
    manager = MapManager(60, 60)
    map_matrix = manager.get_map('world')
    return render_template('base.html', map_matrix=map_matrix)

@app.route('/cave')
def cave():
    manager = MapManager(60, 60)
    map_matrix = manager.get_map('cave')
    return render_template('maps/cave.html', map_matrix=map_matrix)

@app.route('/dungeon')
def dungeon():
    manager = MapManager(60, 60)
    map_matrix = manager.get_map('dungeon')
    return render_template('maps/dungeon.html', map_matrix=map_matrix)

@app.route('/world')
def world():
    manager = MapManager(60, 60)
    map_matrix = manager.get_map('world')
    return render_template('maps/world.html', map_matrix=map_matrix)

if __name__ == '__main__':
    app.run(debug=True)