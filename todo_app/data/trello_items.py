import json
import os

import requests
from flask import session


class TrelloService:
    def __init__(self) -> None:
        self._BOARD_ID = os.environ.get("BOARD_ID")
        self._API_KEY = os.environ.get("TRELLO_API_KEY")
        self._TOKEN = os.environ.get("TRELLO_TOKEN")

        self.api_url = "https://api.trello.com/1"
        self.headers = {"Accept": "application/json"}
        self.auth = {"key": self._API_KEY, "token": self._TOKEN}

        # # Create a dictionary for the bard lists with list_name: list_id
        # This way we can refer to the correct id when moving cards across lists
        # The list_name, list_id values are pretty constant and will remain the same throughout the session.
        # We create this as a variable accessible by all the functions so that we don't have to send the request with each user interaction
        self.list_dict = {}

    def get_cards(self, filter="open"):
        """
        Fetches all saved items from the trello board.

        Args:
            filter: filter items to return by a value

        Returns:
            list: A list of dictionaries, each containing the data of an item.
        """

        self.get_board_lists()

        # build url and send GET request
        url = "/".join([self.api_url, "boards", self._BOARD_ID, "cards"])
        filter_query = {"filter": filter}
        response_query = filter_query | self.auth
        response = requests.get(
            url, headers=self.headers, params=response_query, verify=False
        )
        response_data = response.json()

        # create a list of Item class objects containing only the needed data from each item
        object_list = []
        for item in response_data:
            object_list.append(
                Item(item["id"], item["name"], self.list_dict[item["idList"]])
            )
        return object_list

    # get existing items in trello board
    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of saved items.
        """
        return session.get("items", self.get_cards("open").copy())

    def add_card(self, card_title, list_name="To Do"):
        """
        Creates a new card item, with the specified title and adds it to the 'To Do' list of the specified board

        Args:
            title: the title of the card item.
            list: (optional) name of the specific list to place the new item in
        """

        # find id of "To Do" list using our list_dict
        list_id = [k for k, v in self.list_dict.items() if v == list_name]

        # build url and send POST request
        url = "/".join([self.api_url, "cards"])
        params = {"idList": list_id, "name": card_title} | self.auth
        requests.post(url, headers=self.headers, params=params, verify=False)

    def get_board_lists(self):
        """
        Fetches the data of all the lists in the specified trello board

        Returns:
            List: A list of dictionaries, each containing the data of a list in a board
        """
        url = "/".join([self.api_url, "boards", self._BOARD_ID, "lists"])
        response = requests.get(
            url, headers=self.headers, params=self.auth, verify=False
        )
        response_data = response.json()

        for item in response_data:
            list_id = item["id"]
            list_name = item["name"]
            self.list_dict[list_id] = list_name

    def update_card_status(self, card_id, list_name="Done"):
        """
        Updates the list_id of an existing card in the board.

        Args:
            card_id: id of the card to update
            list_name: (optional) name of the trello list to move the card to
        """

        # find id of the destination list using our list_dict
        dest_list_id = [k for k, v in self.list_dict.items() if v == list_name]

        url = url = "/".join([self.api_url, "cards", card_id])
        params = {"idList": dest_list_id} | self.auth
        requests.put(url, headers=self.headers, params=params, verify=False)


class Item:
    def __init__(self, id, name, status="To Do"):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card["id"], card["name"], list["name"])
