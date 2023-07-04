"""Unit tests for view_model.py """

import pytest
from todo_app.data.view_model import ViewModel
from todo_app.data.trello_items import Item

def test_view_model_done_property():
    test_item = Item(123456789, "test_item", "Done")
    view_model = ViewModel(test_item).done_items
    assert(view_model.items.status == "Done")
   

