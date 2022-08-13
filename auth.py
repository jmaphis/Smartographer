from flask import Flask, g, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
