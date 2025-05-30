import requests
import dotenv
import os
from agno.tools import tool
from typing import List, Optional
from backend.schemas import TrelloCard

dotenv.load_dotenv()
BASE_URL = "https://api.trello.com/1"


def get_auth_params():
    return {"key": os.getenv("TRELLO_API_KEY"), "token": os.getenv("TRELLO_TOKEN")}


def get_board_id():
    return os.getenv("BOARD_ID")


def request(method, endpoint, params=None, json=None):
    url = f"{BASE_URL}{endpoint}"
    if params is None:
        params = {}
    params.update(get_auth_params())
    response = requests.request(method, url, params=params, json=json)
    response.raise_for_status()
    return response.json()


# Boards
def get_boards(member_id="me"):
    """Get all boards for a member."""
    return request("GET", f"/members/{member_id}/boards")


def get_board(board_id):
    """Get a single board by ID."""
    return request("GET", f"/boards/{board_id}")


def get_board_cards(board_id):
    """Get a single board by ID."""
    return request("GET", f"/boards/{board_id}/cards")


def get_lists_on_board(board_id):
    """Get all lists on a board."""
    return request("GET", f"/boards/{board_id}/lists")


def get_list(list_id):
    """Get a single list by ID."""
    return request("GET", f"/lists/{list_id}")


# Cards
def get_cards_on_list(list_id):
    """Get all cards on a list."""
    return request("GET", f"/lists/{list_id}/cards")


def get_card(card_id):
    """Get a single card by ID."""
    return request("GET", f"/cards/{card_id}")


@tool(
    name="get_trello_list_names",  # Custom name for the tool (otherwise the function name is used)
    description="gets names of existing lists on board ",  # Custom description (otherwise the function docstring is used)
    show_result=False,  # Show result after function call
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent                     # Hook to run before and after execution
    requires_confirmation=False,  # Requires user confirmation before execution
    cache_results=False,  # Cache TTL in seconds (1 hour)
)
def get_trello_list_names() -> List[str]:
    """
    Fetch the names of all existing lists on the current Trello board.

    This function makes a GET request to the Trello API to retrieve the lists associated
    with the currently active board, identified by `get_board_id()`. It extracts the "name"
    field from each list object in the response and returns them as a list of strings.

    Returns:
        List[str]: A list containing the names of all lists on the current Trello board.
                   Only items with a "name" field will be included in the result.
    """
    board = request("GET", f"/boards/{get_board_id()}/lists")
    return [item["name"] for item in board if "name" in item]


@tool(
    name="trello_search",  # Custom name for the tool (otherwise the function name is used)
    description="get cards from trello from a query ",  # Custom description (otherwise the function docstring is used)
    show_result=False,  # Show result after function call
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent                     # Hook to run before and after execution
    requires_confirmation=False,  # Requires user confirmation before execution
    cache_results=False,  # Cache TTL in seconds (1 hour)
)
def trello_search(
    query: Optional[str] = None, listName: Optional[str] = None
) -> TrelloCard:
    """
    Fetch Trello cards either by a search query (keyword) or by retrieving all cards on the board.

    This function queries the Trello API to fetch cards based on the provided `query`.
    If `query` is not provided, it retrieves all cards from the current Trello board.
    The results are formatted using the `formatResponse` function.

    You can control which fields are included in each returned card dictionary using the `listName` parameter.
    This parameter should be a comma-separated string containing the desired field names (e.g., "name,due,desc").
    Only the specified fields will be included in each result object.

    Valid field names and their meanings:

        - "comments"              (int):        Number of comments on the card
        - "commentDescription"   (str):        Text description related to comments
        - "due"                   (str | None): Due date in ISO 8601 format or `None`
        - "start"                 (str | None): Start date in ISO 8601 format or `None`
        - "dueReminder"           (str | None): Reminder date/time in ISO format or `None`
        - "dueComplete"           (bool):       Whether the due date has been marked as complete
        - "email"                 (str | None): Email address associated with the card, or `None`
        - "listName"                (str):        ID of the list this card belongs to
        - "name"                  (str):        Title or name of the card
        - "desc"                  (str):        Detailed description of the card
        - "dateLastActivity"      (str | None): Timestamp of the last activity on the card (ISO 8601 format) or `None`
        - "closed"                (bool):       Whether the card is archived

    **Notes**:
    - Do NOT use commit hash as `query`.
    - If the API failed or response was empty array call it with no args and get all cards
    - These fields map directly from the Trello API response.
    - If the API field is `null`, it will be returned as `None` in Python.
    - Date fields are returned as ISO 8601 strings (e.g., "2024-05-29T13:45:00.000Z").
    - If `listName` is not provided, all available fields will be returned for each card.

    Args:
        query (Optional[str]): Partial keywords of the cards to search for matching Trello cards.
                            If omitted, all cards on the board will be returned.
        listName (Optional[str]):A comma-separated string specifying the names of card lists to include.
                          If None, cards from all available lists will be included.


    Returns:
        list[dict]: A list of dictionaries, each representing a Trello card.
                    Keys are the field names, and values match the expected types above.
                    If a field is `null`in the Trello API, it will appear as `None` in the result.
    """
    if listName:
        requestedItems = listName.split(",")
    else:
        requestedItems = None
    if not query:
        return formatResponse(get_board_cards(get_board_id()), requestedItems)
    else:
        return trello_search_partial(query, requestedItems)


def trello_search_partial(query: str, listName: Optional[list] = None):
    searchCards = request(
        "GET", "/search", {"partial": "true", "query": query, "modelTypes": "cards"}
    )
    return formatResponse(searchCards["cards"], listName)


def formatResponse(info, listName: Optional[List[str]] = None):
    res = []
    listIdDictionary = {}
    for item in info:
        list_id = item["idList"]
        if list_id in listIdDictionary:
            list_name = listIdDictionary[list_id]
        else:
            list_name = get_list(list_id)["name"]
            listIdDictionary[list_id] = list_name
            item["idList"] = list_name
        full_card_data = {
            "comments": item["badges"]["comments"],
            "commentDescription": item["badges"]["description"],
            "due": item["due"],
            "email": item.get("email"),
            "listName": item["idList"],
            "name": item["name"],
            "start": item["start"],
            "dueReminder": item["dueReminder"],
            "desc": item["desc"],
            "dateLastActivity": item["dateLastActivity"],
            "dueComplete": item["dueComplete"],
            "closed": item["closed"],
        }
        if listName is None or full_card_data["listName"] in listName:
            res.append(full_card_data)

    return res


# resp=get_trello_list_names()
# print(trello_search(listName=resp[0]))
# print(resp)
