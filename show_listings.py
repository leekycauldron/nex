import requests
from dotenv import load_dotenv
import os

load_dotenv()

MIN_PRICE = 20
MAX_PRICE = 100
MIN_LIQUIDITY = 50
MIN_SPREAD = 24 # as a percentage (%)

def show_listings():
    print("Fetching CSFloat listings...")
    response = requests.get(f"""https://api.pricempire.com/v4/paid/items/prices?api_key={os.getenv('PRICE_EMPIRE_API_KEY')}&sources=csfloat,buff163&currency=CAD""")

    first_filter = {}

    for item in response.json():
        try:    
            name = item.get('market_hash_name')
            liquidity = item.get('liquidity',"0")
            if liquidity is None:
                liquidity = 0
            liquidity = int(liquidity)
            csfloat_price = float(item.get('prices')[0].get('price')/100 if item.get('prices') and item.get('prices')[0].get('price') else 0)
            buff163_price = float(item.get('prices')[1].get('price')/100 if item.get('prices') and item.get('prices')[1].get('price') else 0)

            spread = 0 
            if csfloat_price != 0 and buff163_price != 0:
                spread = ((csfloat_price - buff163_price) / buff163_price) * 100

            if liquidity >= MIN_LIQUIDITY and \
                MIN_PRICE <  csfloat_price < MAX_PRICE and \
                spread > MIN_SPREAD:
                first_filter[name] = {"liquidity": f"{liquidity}%", "csfloat_price": f"${csfloat_price}", "buff163_price": f"${buff163_price}", "spread": f"{spread:.2f}%"}
        except Exception as e:
            print(e)
            print(item)
            break



    for name, data in first_filter.items():
        print(f"{name} -- Price (CS Float): {data['csfloat_price']} CAD -- Price (Buff 163): {data['buff163_price']} CAD -- Spread: {data['spread']}")