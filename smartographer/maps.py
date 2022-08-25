from smartographer.utilities.mapmanager import MapManager

from smartographer.db import get_db
from smartographer.auth import login_required

from markupsafe import escape
from flask import Blueprint, render_template, session, redirect, url_for, request

bp = Blueprint('maps', __name__, url_prefix='/maps')

def get_tag_list(type):
    # creates a list of anchor tags, starting with the refresh button
    refresh_url = url_for('maps.refresh_map', **{'type': type})
    save_url = url_for('maps.save', **{'type': type})
    tag_list = []
    tag_list.append('<a href="' + refresh_url + '">Refresh</a>')
    tag_list.append('<a href="' + save_url + '">Save</a>')
    # adds anchor tags to the list for the other maps
    for other in ['cave', 'dungeon', 'world']:
        if other != type:
            map_url = url_for('maps.get_map', **{'type': other})
            tag_list.append(
                '<a href="' + map_url + '">' + other.capitalize() + ' Map</a>'
                )
    return tag_list

@bp.route('/<type>', methods=('GET', 'POST'))
def get_map(type):
    type = escape(type)
    # creates a list of anchor tags, starting with the refresh button
    tag_list = get_tag_list(type)
    seed = session.get(type + '_seed')
    manager = MapManager(60, 60, seed=seed)
    current_map = manager.get_map(type)
    session[type + '_map'] = current_map
    session[type + '_seed'] = manager.get_seed()
    return render_template('maps/get_map.html', current_map=current_map, 
                                            type=type, tag_list=tag_list)

@bp.route('/refresh_<type>')
def refresh_map(type):
    type = escape(type)
    session[type + '_seed'] = None
    return redirect(url_for('maps.get_map', type=type))

@bp.route('/<type>/save', methods=('GET', 'POST'))
@login_required
def save(type):
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
    get_map(type)
    current_map = session[type + '_map']
    tag_list =  get_tag_list(type)
    return render_template('maps/save.html', current_map=current_map,
                                        tag_list=tag_list, type=type)

@bp.route('/load')
@login_required
def load():
    db = get_db()
    user_id = session.get('user_id')
    loaded_maps = db.execute(
            'SELECT * FROM map'
        ).fetchall()

    return render_template('maps/load.html', loaded_maps=loaded_maps)

@bp.route('/<type>/<seed>')
def set_seed(type, seed):
    seed = escape(seed)
    session[type + '_seed'] = seed
    return redirect(url_for('maps.get_map', type=type))

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute('DELETE FROM map WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('map.load'))