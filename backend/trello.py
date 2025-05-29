import requests
import dotenv
import os
from typing import Optional
dotenv.load_dotenv()
BASE_URL = "https://api.trello.com/1"

def get_auth_params():
    return {
        "key": os.getenv("TRELLO_API_KEY"),
        "token": os.getenv("TRELLO_TOKEN")
    }

def get_board_id():
    return os.getenv("BOARD_ID")

def request( method, endpoint, params=None, json=None):
    url = f"{BASE_URL}{endpoint}"
    if params is None:
        params = {}
    params.update(get_auth_params())
    response = requests.request(method, url, params=params, json=json)
    response.raise_for_status()
    return response.json()

# Boards
def get_boards( member_id='me'):
    """Get all boards for a member."""
    return request("GET", f"/members/{member_id}/boards")

def get_board( board_id):
    """Get a single board by ID."""
    return request("GET", f"/boards/{board_id}")

def get_board_cards( board_id):
    """Get a single board by ID."""
    return request("GET", f"/boards/{board_id}/cards")

def get_lists_on_board( board_id):
    """Get all lists on a board."""
    return request("GET", f"/boards/{board_id}/lists")

def get_list( list_id):
    """Get a single list by ID."""
    return request("GET", f"/lists/{list_id}")

# Cards
def get_cards_on_list( list_id):
    """Get all cards on a list."""
    return request("GET", f"/lists/{list_id}/cards")

def get_card( card_id):
    """Get a single card by ID."""
    return request("GET", f"/cards/{card_id}")

def trello_search(query:Optional[str]=None,listName:Optional[list]=None):
    if not query:
        return get_board_cards(get_board_id())
    else:
        return trello_search_partial(query,listName) 

def trello_search_partial(query:str,listName:Optional[list]=None):
    searchCards= request('GET',"/search",
                   {
                       "partial":"true" ,
                       "query":query,
                       "modelTypes": "cards"  
                    }
                )
    listIdDictionary={}
    res=[]
    for item in searchCards["cards"]:
        list_id = item["idList"]

        if list_id in listIdDictionary:
            list_name = listIdDictionary[list_id]
        else:
            list_name = get_list(list_id)["name"]
            listIdDictionary[list_id] = list_name

        full_card_data = {
            "comments": item["badges"]["comments"],
            "comment-description": item["badges"]["description"],
            "due": item["due"],
            "email": item.get("email"),
            "listId": list_name,
            "name": item["name"],
            "start": item["start"],
            "dueReminder": item["dueReminder"],
            "desc": item["desc"],
            "dateLastActivity": item["dateLastActivity"],
            "dueComplete": item["dueComplete"],
            "closed": item["closed"]
        }

        if listName is None:
            res.append(full_card_data)
        else:
            print("here")
            filtered_card_data = {key: value for key, value in full_card_data.items() if key in listName}
            res.append(filtered_card_data)
    return res

resp=trello_search("research")
print(resp)