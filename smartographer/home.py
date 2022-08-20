from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from smartographer.auth import login_required
from smartographer.db import get_db

bp = Blueprint('index', __name__)

@bp.route('/')
def home():
    return render_template('home.html')