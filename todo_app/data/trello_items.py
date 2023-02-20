import json
import os
from flask import session

import requests
#For testing purposes only 
from dotenv import load_dotenv
load_dotenv()

# _HTTP_PROXY=str(os.getenv('HTTP_PROXY'))
# _HTTPS_PROXY=str(os.getenv('HTTPS_PROXY'))

_HTTP_PROXY=os.getenv('HTTP_PROXY')
_HTTPS_PROXY=os.getenv('HTTPS_PROXY')

_BOARD_ID = os.environ.get('BOARD_ID')
_API_KEY = os.environ.get('TRELLO_API_KEY')
_TOKEN = os.environ.get('TRELLO_TOKEN')


api_url = "https://api.trello.com/1"
headers = {"Accept": "application/json"}
auth = {
    'key': _API_KEY,
    'token': _TOKEN
}

def get_board_info():
    """
    Fetches the board info of _BOARD_ID

    Returns:
        Dictionary: A dictionary containing all the data on the specified board
    """
    url = "/".join([api_url, "boards", _BOARD_ID])
    response = requests.get(url, headers=headers, params=auth, verify=False)
    response_data = json.loads(response.text)
    return response_data

def get_cards(filter="open"):
    """
    Fetches all saved items from the trello board.

    Args:
        filter: filter items to return by a value

    Returns:
        list: A list of dictionaries, each containing the data of an item.
    """
    #build url and send GET request
    url = "/".join([api_url, "boards", _BOARD_ID, "cards"])
    filter_query = {'filter': filter}
    response_query = filter_query | auth
    response = requests.get(url, headers=headers, params=response_query, verify=False)
    response_data = json.loads(response.text)

    # create a list of dictionaries containing the needed data from each item
    clean_data = []
    for item in response_data:
        item_dictionary = {'id': item['id'], 'title': item['name'], 'desc': item['desc'], 'idList': item['idList'],'closed_status': item['closed'] }
        clean_data.append(item_dictionary)
    return(clean_data)

#get existing items in trello board
def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get('items', get_cards('open').copy())

def add_card(card_title, list_name="To Do"):
    """
    Creates a new item, with the specified title and adds it to the 'To Do' list of the specified board

    Args:
        title: the title of the item.
        list: (optional) name of the specific list to place the new item in

    Returns: (none?)
        item: A dictionary containing the data of the created item.
    """

    # request id of "To Do" list
    board_lists = get_board_lists()
    todo_list = next((item for item in board_lists if item['name'] == list_name), None)

    #build url and send POST request
    url = "/".join([api_url, "cards"])
    params = {'idList': todo_list["id"], 'name': card_title} | auth
    response = requests.post(url, headers=headers, params=params, verify=False)
    return response

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

def get_to_do_cards():
    """
    Fetches all the 'To Do' cards from the specified trello board

    Returns:
        list: A list of dictionaries, each containing the data of an item
    """
    
    #find all cards on a board
    pass

def update_card_status(card_id):
    """
    Updates the list_id of an existing card in the board. If no existing card matches the card_id specified. nothing is done.

    Args:
        card_id: id of the card to update
    """
    pass

# for testing purposes only
if __name__ == "__main__":
    get_board_info()
    get_board_lists()
    print(get_cards())

