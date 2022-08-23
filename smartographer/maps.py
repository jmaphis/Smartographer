from smartographer.utilities.mapmanager import MapManager
from smartographer.utilities.array_int_conversion import (
    array_to_int, int_to_array
)
from smartographer.db import get_db
from smartographer.auth import login_required

from markupsafe import escape
from flask import Blueprint, render_template, session, redirect, url_for, request

bp = Blueprint('maps', __name__, url_prefix='/maps')

@bp.route('/<type>', methods=('GET', 'POST'))
def get_map(type):
    type = escape(type)
    if request.method == 'POST':
        map_array = session[type + '_map']
        map_name = escape(request.form['mapname'])

        db = get_db()
        db.execute(
            "INSERT INTO map (map, type, name, user_id) VALUES (?, ?, ?, ?)",
            (map_array, type, map_name, session['user_id'])
        )
        return redirect(url_for('maps.get_map', type=type))

    # creates a list of anchor tags, starting with the refresh button
    refresh_url = url_for('maps.refresh_map', **{'type': type})
    tag_list = []
    tag_list.append('<a href="' + refresh_url + '">Refresh</a>')
    # adds anchor tags to the list for the other maps
    for other in ['cave', 'dungeon', 'world']:
        if other != type:
            map_url = url_for('maps.get_map', **{'type': other})
            tag_list.append(
                '<a href="' + map_url + '">' + other.capitalize() + ' Map</a>'
                )
        pass
    if not session.get(type + '_map'):
        manager = MapManager(60, 60)
        current_map = manager.get_map(type)
        session[type + '_map'] = current_map
        return render_template('maps/get_map.html', current_map=current_map, 
                                                    tag_list=tag_list)
    else: 
        current_map = session[type + '_map']
        return render_template('maps/get_map.html', current_map=current_map, 
                                                    tag_list=tag_list)

@bp.route('/refresh_<type>')
def refresh_map(type):
    type = escape(type)
    session[type + '_map'] = None
    return redirect(url_for('maps.get_map', type=type))

@bp.route('/load')
@login_required
def load():
    db = get_db()
    user_id = session.get('user_id')
    loaded_maps = db.execute(
            'SELECT * FROM map WHERE author_id = ?', (user_id,)
        ).fetchall()

    return render_template('maps/load.html', loaded_maps=loaded_maps)