import requests
import json
from PIL import Image, ImageDraw, ImageFont
import urllib.request
from discohook.client import Discohook
from config import *


# Get the data from the API
def search_market(query, count=100):
    url = f"https://steamcommunity.com/market/search/render?norender=1&query={query}&search_descriptions=1&category_440_Collection[]=any&category_440_Type[]=any&appid=440&count={count}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def generate_item_row(item):
    font = "arialbd.ttf"
    w, h = 500, 76

    avatar = Image.open(urllib.request.urlopen(f'https://community.cloudflare.steamstatic.com/economy/image/{item["asset_description"]["icon_url"]}/62fx62f'))

    img = Image.new("RGB", (w, h), color = (22, 32, 45))
    ImageDraw.Draw(img).rectangle((6, 6, 70, 70), fill=(60, 53, 46),outline="#"+item["asset_description"]["name_color"])
    img.paste(avatar, (6, 6),mask=avatar)
    ImageDraw.Draw(img).text((80, 21), item["name"], fill="#"+item["asset_description"]["name_color"], font=ImageFont.truetype(font, 14))
    ImageDraw.Draw(img).text((80, 39), item["app_name"], fill=(143, 152, 160), font=ImageFont.truetype(font, 12))
    ImageDraw.Draw(img).text((w-91, 25), item["sell_price_text"], fill=(164, 208, 7), font=ImageFont.truetype(font, 20))
    return img

def send_discord_webhook(message):
    webhook = Discohook(url=webhook_url, username="Steam Market", avatar_url="https://cdn.freebiesupply.com/images/large/2x/steam-logo-transparent.png")

    with open("img.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='example.jpg')
    webhook.content = message

    webhook.execute()


data = search_market(search_query, 100)

# List of all the items according to their price
items = data["results"]
items = sorted(items, key=lambda item: item["sell_price"])

with open("items.json", "r") as f:
    stored_items = json.load(f)
for i, item in enumerate(items):
    if f'{item["asset_description"]["classid"]}_{item["asset_description"]["instanceid"]}' in stored_items:
        continue
    stored_items.append(f'{item["asset_description"]["classid"]}_{item["asset_description"]["instanceid"]}')

    img = generate_item_row(item)
    img.save(f"img.png")
    send_discord_webhook(f"<@&{ping_role}> | New item found: ``{item['name']}``")

with open("items.json", "w") as f:
    json.dump(stored_items, f)