import json
import os

import requests
from flask import session


def get_cards(filter="open"):
    """
    Fetches all saved items from the trello board.

    Args:
        filter: filter items to return by a value

    Returns:
        list: A list of dictionaries, each containing the data of an item.
    """

    # build url and send GET request
    url = "/".join([api_url, "boards", _BOARD_ID, "cards"])
    filter_query = {"filter": filter}
    response_query = filter_query | auth
    response = requests.get(url, headers=headers, params=response_query, verify=False)
    response_data = json.loads(response.text)

    # create a list of Item class objects containing only the needed data from each item
    object_list = []
    for item in response_data:
        if list_dict[item["idList"]] == "To Do":
            object_list.append(
                Item(item["id"], item["name"], list_dict[item["idList"]])
            )
    return object_list


# get existing items in trello board
def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get("items", get_cards("open").copy())


def add_card(card_title, list_name="To Do"):
    """
    Creates a new card item, with the specified title and adds it to the 'To Do' list of the specified board

    Args:
        title: the title of the card item.
        list: (optional) name of the specific list to place the new item in
    """

    # find id of "To Do" list using our list_dict
    list_id = [k for k, v in list_dict.items() if v == list_name]

    # build url and send POST request
    url = "/".join([api_url, "cards"])
    params = {"idList": list_id, "name": card_title} | auth
    requests.post(url, headers=headers, params=params, verify=False)


def get_board_lists():
    """
    Fetches the data of all the lists in the specified trello board

    Returns:
        List: A list of dictionaries, each containing the data of a list in a board
    """
    url = "/".join([api_url, "boards", _BOARD_ID, "lists"])
    response = requests.get(url, headers=headers, params=auth, verify=False)
    response_data = json.loads(response.text)
    return response_data


def update_card_status(card_id, list_name="Done"):
    """
    Updates the list_id of an existing card in the board.

    Args:
        card_id: id of the card to update
        list_name: (optional) name of the trello list to move the card to
    """

    # find id of the destination list using our list_dict
    dest_list_id = [k for k, v in list_dict.items() if v == list_name]

    url = url = "/".join([api_url, "cards", card_id])
    params = {"idList": dest_list_id} | auth
    requests.put(url, headers=headers, params=params, verify=False)


_BOARD_ID = os.environ.get("BOARD_ID")
_API_KEY = os.environ.get("TRELLO_API_KEY")
_TOKEN = os.environ.get("TRELLO_TOKEN")

api_url = "https://api.trello.com/1"
headers = {"Accept": "application/json"}
auth = {"key": _API_KEY, "token": _TOKEN}

# Create a dictionary for the bard lists with list_name: list_id
# This way we can refer to the correct id when moving cards across lists
# The list_name, list_id values are pretty constant and will remain the same throughout the session.
# We create this as a variable accessible by all the functions so that we don't have to send the request with each user interaction
board_lists = get_board_lists()
list_dict = {}
for item in board_lists:
    list_id = item["id"]
    list_name = item["name"]
    list_dict[list_id] = list_name


class Item:
    def __init__(self, id, name, status="To Do"):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card["id"], card["name"], list["name"])
