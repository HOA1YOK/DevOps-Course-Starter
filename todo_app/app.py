from urllib import request
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

@app.route('/action', methods=['POST', 'GET'])
def action():
    new_item = request.form.get('item')
    add_item(new_item)
    return redirect(url_for(".index"))