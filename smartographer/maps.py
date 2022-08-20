from smartographer.mapmanager import MapManager
from smartographer.db import get_db
from smartographer.auth import login_required

import sqlite3
from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint('maps', __name__, url_prefix='/maps')

@bp.route('/cave')
def cave():
    if not session.get('cave_map'):
        manager = MapManager(60, 60)
        cave_map = manager.get_map('cave')
        session['cave_map'] = cave_map
        return render_template('maps/cave.html', cave_map = cave_map)
    else: 
        cave_map = session['cave_map']
        return render_template('maps/cave.html', cave_map=cave_map)

@bp.route('/dungeon')
def dungeon():
    if not session.get('dungeon_map'):
        manager = MapManager(60, 60)
        dungeon_map = manager.get_map('dungeon')
        session['dungeon_map'] = dungeon_map
        return render_template('maps/dungeon.html', dungeon_map=dungeon_map)
    else: 
        dungeon_map = session['dungeon_map']
        return render_template('maps/dungeon.html', dungeon_map=dungeon_map)

@bp.route('/world')
def world():
    if not session.get('world_map'):
        manager = MapManager(60, 60)
        world_map = manager.get_map('world')
        session['world_map'] = world_map
        return render_template('maps/world.html', world_map=world_map)
    else: 
        world_map = session["world_map"]
        return render_template('maps/world.html', world_map=world_map)

@bp.route('/refresh_cave')
def refresh_cave():
    session['cave_map'] = None
    return redirect(url_for('maps.cave'))

@bp.route('/refresh_dungeon')
def refresh_dungeon():
    session['dungeon_map'] = None
    return redirect(url_for('maps.dungeon'))

@bp.route('/refresh_world')
def refresh_world():
    session['world_map'] = None
    return redirect(url_for('maps.world'))

@bp.route('/save')
@login_required
def save(map, type):
    pass
