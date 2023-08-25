"""Unit tests for view_model.py """

import pytest

from todo_app.data.trello_items import Item
from todo_app.data.view_model import ViewModel

_TEST_ITEMS = [
    Item(100000, "test_item", "Doing"),
    Item(200000, "test_item", "Done"),
    Item(300000, "test_item", "To Do"),
    Item(400000, "test_item", "Done"),
]


def test_view_model_done_property():
    view_model = ViewModel(_TEST_ITEMS).done_items
    for i in view_model:
        assert i.status == "Done"
    assert len(view_model) == 2


def test_view_model_todo_property():
    view_model = ViewModel(_TEST_ITEMS).todo_items
    for i in view_model:
        assert i.status == "To Do"


def test_view_model_doing_property():
    view_model = ViewModel(_TEST_ITEMS).doing_items
    for i in view_model:
        assert i.status == "Doing"
