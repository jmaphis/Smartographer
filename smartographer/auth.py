from smartographer.db import get_db

from flask import(
    g, redirect, render_template, request, url_for, flash, session, Blueprint
)
from werkzeug.security import check_password_hash, generate_password_hash

import functools

def get_tag_list(type=None, is_map=False):
    # creates a list of anchor tags, starting with the refresh button
    tag_list = []
    tag_list.append('<div class="nav-tags">')
    if is_map:
        refresh_url = url_for('maps.refresh_map', **{'type': type})
        tag_list.append('<a href="' + refresh_url + '">Refresh</a>')
    # adds anchor tags to the list for the other maps
    for other in ['cave', 'dungeon', 'world']:
        if other != type:
            map_url = url_for('maps.get_map', **{'type': other})
            tag_list.append(
                '<a href="' + map_url + '">' + other.capitalize() + '</a>'
                )

    load_url = url_for('maps.load')
    tag_list.append('<a href="' + load_url + '">Load</a>')
    if is_map:
        tag_list.append('''
            </div>
            <form class="save-form" method="post">
                <input type="submit" value="Save">
                <label for="mapname">Map Name:</label>
                <input name="mapname" id="mapname" required>
            </form>
        ''')
    return tag_list

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Please enter a username.'
        elif not password:
            error = 'Please enter a password.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = "That username is already registered."
            else:
                return redirect(url_for("auth.login"))

        else:
            flash(error)

    tag_list = get_tag_list()
    return render_template('auth/register.html', tag_list=tag_list)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        else:
            flash(error)

    tag_list = get_tag_list()
    return render_template('auth/login.html', tag_list=tag_list)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view