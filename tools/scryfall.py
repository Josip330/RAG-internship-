from langchain_core.tools import tool
import requests
import os


@tool
def get_card_by_name(name: str) -> str:
    """
    Fetches a Magic: The Gathering card by name from Scryfall and returns a textual summary.
    """
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        type_line = data['type_line']
        oracle_text = data.get('oracle_text', 'No rules text available.')
        image_url = data['image_uris']['normal']
        return (
            f"{name}\n"
            f"Type: {type_line}\n"
            f"Text: {oracle_text}\n"
        )
    else:
        return "Card not found."
