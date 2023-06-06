from flask import Flask, redirect, render_template, request, url_for

from todo_app.data.trello_items import add_card, get_items, update_card_status
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


# Display list of items
@app.route("/")
def index():
    items = get_items()
    return render_template("index.html", items=items)


# Create new items
@app.post("/action")
def action():
    new_item = request.form.get("item")
    add_card(new_item)
    return redirect(url_for(".index"))


# Change item status
@app.post("/complete-item")
def complete_item():
    complete_item = request.form.get("complete_item")
    update_card_status(complete_item, "Done")
    return redirect(url_for(".index"))
