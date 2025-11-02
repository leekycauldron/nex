import requests
from dotenv import load_dotenv
from tabulate import tabulate
import os

load_dotenv()


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


headers = ["Name", "Original Price (CAD$)", "Current Price (CAD$)", "Unrealized Gain(Loss) (%)"]

def get_watchlist():
    with open("watchlist.txt","r") as f:
        items = f.readlines()
    sanitized_items = [i.strip().split("\t") for i in items]
    for item in sanitized_items:
        item[1] = float(item[1][3:])
    return sanitized_items


def get_csfloat_items():
    r = requests.get(f"""https://api.pricempire.com/v4/paid/items/prices?api_key={os.getenv('PRICE_EMPIRE_API_KEY')}&sources=csfloat&currency=CAD""")
    names_and_prices = {}
    for item in r.json():  
        names_and_prices[item.get('market_hash_name')] = float(item.get('prices')[0].get('price')/100 if item.get('prices') and item.get('prices')[0].get('price') else 0)
    return names_and_prices


def show_watchlist():
    print("Fetching current watchlist prices...")
    items = get_watchlist()
    csfloat_items = get_csfloat_items()

    data = []

    for item in items:
        to_add = [item[0], item[1]]
        if item[0] in csfloat_items.keys():
            current_price = csfloat_items[item[0]]
            to_add.append(current_price)
            spread = (current_price-item[1]) / item[1] * 100
            if spread < 0:
                spread = f"{RED}{spread:.2f}{RESET}"
            else:
                spread = f"{GREEN}{spread:.2f}{RESET}"
            to_add.append(spread)
        else:
            to_add.extend(["N/A","N/A"])
        data.append(to_add)

    print(tabulate(data, headers, tablefmt="fancy_grid", stralign="center"))
