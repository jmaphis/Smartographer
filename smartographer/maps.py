from smartographer.utilities.mapmanager import MapManager
from smartographer.db import get_db
from smartographer.auth import login_required

from markupsafe import escape
from flask import Blueprint, render_template, session, redirect, url_for, request

from random import randrange

SEED_LIMIT = 9999999

bp = Blueprint('maps', __name__, url_prefix='/maps')

def get_tag_list(type=None, is_map=False):
    # creates a list of anchor tags, starting with the refresh button
    tag_list = []
    if is_map:
        refresh_url = url_for('maps.refresh_map', **{'type': type})
        tag_list.append('<a href="' + refresh_url + '">Refresh</a>')
    # adds anchor tags to the list for the other maps
    for other in ['cave', 'dungeon', 'world']:
        if other != type:
            map_url = url_for('maps.get_map', **{'type': other})
            tag_list.append(
                '<a href="' + map_url + '">' + other.capitalize() + ' Map</a>'
                )

    load_url = url_for('maps.load')
    tag_list.append('<a href="' + load_url + '">Load Map</a>')
    if is_map:
        tag_list.append('''
            <form method="post">
                <input type="submit" value="Save Map">
                <label for="mapname">Map Name:</label>
                <input name="mapname" id="mapname" required>
            </form>
        ''')
    return tag_list

def generate_seed():
    seed = randrange(SEED_LIMIT)
    return seed

@bp.route('/<type>', methods=('GET', 'POST'))
def get_map(type):
    type = escape(type)
    if request.method == 'POST':
        name = escape(request.form['mapname'])
        db = get_db()
        db.execute(
            "INSERT INTO map (seed, type, name, user_id) VALUES (?, ?, ?, ?)",
            (session[type + '_seed'], type, name, session['user_id'])
        )
        db.commit()
        return redirect(url_for('maps.get_map', type=type))
    # creates a list of anchor tags, starting with the refresh button
    tag_list = get_tag_list(type=type, is_map=True)
    if not session.get(type + '_seed'):
        seed = generate_seed()
        return redirect(url_for('maps.set_seed', type=type, seed=seed))
    manager = MapManager(60, 60, session[type + '_seed'])
    current_map = manager.get_map(type)
    session[type + '_map'] = current_map
    return render_template('maps/get_map.html', current_map=current_map, 
                                            type=type, tag_list=tag_list)

@bp.route('/refresh_<type>')
def refresh_map(type):
    type = escape(type)
    seed = generate_seed()
    return redirect(url_for('maps.set_seed', type=type, seed=seed))

@bp.route('/load', methods=('GET','POST'))
@login_required
def load():
    tag_list = get_tag_list()
    if request.method == ['DELETE']:
        db = get_db()
        db.execute('DELETE FROM map WHERE id = ?', (id,))
        db.commit()
    db = get_db()
    user_id = session.get('user_id')
    loaded_maps = db.execute(
            'SELECT * FROM map WHERE user_id = ?', (user_id,)
        ).fetchall()

    return render_template('maps/load.html', loaded_maps=loaded_maps, tag_list=tag_list)

@bp.route('/<type>/<seed>')
def set_seed(type, seed):
    session[type + '_seed'] = seed
    return redirect(url_for('maps.get_map', type=type))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM map WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('maps.load'))
