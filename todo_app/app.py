from flask import Flask, redirect, render_template, request, url_for

from todo_app.data.session_items import add_item, get_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

# Display list of items
@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

# Create new items
@app.post('/action')
def action():
    new_item = request.form.get('item')
    add_item(new_item)
    return redirect(url_for(".index"))