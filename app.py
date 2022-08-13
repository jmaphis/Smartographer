# Smartographer - A map making web application by James Maphis.
# Uses various algorithms to generate maps for all of your adventuring needs!

from flask import Flask, render_template, request
# from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)