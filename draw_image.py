from PIL import Image, ImageDraw, ImageFont
import urllib.request
import os


item = {
    "name": "Genuine Wilson Weave",
    "app_name": "Team Fortress 2",
    "sell_price": 10806,
    "sell_price_text": "$10.06",
    "asset_description": {
        "background_color": "3C352E",
        "icon_url": "fWFc82js0fmoRAP-qOIPu5THSWqfSmTELLqcUywGkijVjZULUrsm1j-9xgEfZA4UWyTxtjFTjdrZBf2DDN8Mmsgy4N5TiGI5x1J4Z7LtYTRmc1XGVvYLXvBuo1juXyRqvZ4wA9Sw9LhRfVrqqsKYZIyt4iAi",
        "name_color": "4D7455"
    }
}
item = {"name":"Strange Ghastlierest Gibus","hash_name":"Strange Ghastlierest Gibus","sell_listings":1,"sell_price":50209,"sell_price_text":"$502.09","app_icon":"https:\/\/cdn.cloudflare.steamstatic.com\/steamcommunity\/public\/images\/apps\/440\/e3f595a92552da3d664ad00277fad2107345f743.jpg","app_name":"Team Fortress 2","asset_description":{"appid":440,"classid":"4400938331","instanceid":"4424124292","background_color":"3C352E","icon_url":"IzMF03bi9WpSBq-S-ekoE33L-iLqGFHVaU25ZzQNQcXdEH9myp0erksICfTYffEcEJhnqWSMU5OD2NgLxXcNnChXOjLx2Sk5MbUqMcbBnQz4ruyeU3X7ZAjAICzQEl98FOwAWjq2qmb4uoLIE3qeFPYsRV9QL6oEoGIYbs7abRpu1o9f_Dfow0d5S0QtIcEfIVa4nnFCYrkghjEcIsZ91DM0","tradable":1,"name":"Strange Ghastlierest Gibus","name_color":"CF6A32","type":"Strange Hat - Points Scored: 0","market_name":"Strange Ghastlierest Gibus","market_hash_name":"Strange Ghastlierest Gibus","commodity":0},"sale_price_text":"$480.26"}

def generate_item_row(item):
    font = "arialbd.ttf"
    w, h = 500, 76

    i = item["asset_description"]["icon_url"]
    avatar = Image.open(urllib.request.urlopen(f"https://community.cloudflare.steamstatic.com/economy/image/{i}/62fx62f"))

    img = Image.new("RGB", (w, h), color = (22, 32, 45))
    ImageDraw.Draw(img).rectangle((6, 6, 70, 70), fill=(60, 53, 46),outline="#"+item["asset_description"]["name_color"])
    img.paste(avatar, (6, 6),mask=avatar)
    ImageDraw.Draw(img).text((80, 21), item["name"], fill="#"+item["asset_description"]["name_color"], font=ImageFont.truetype(font, 14))
    ImageDraw.Draw(img).text((80, 39), item["app_name"], fill=(143, 152, 160), font=ImageFont.truetype(font, 12))
    ImageDraw.Draw(img).text((w-91, 25), item["sell_price_text"], fill=(164, 208, 7), font=ImageFont.truetype(font, 20))
    return img

def generate_item_list(items):
    w, h = 500, 76
    img = Image.new("RGB", (w, len(items)*h), color = (22, 32, 45))
    for i, item in enumerate(items):
        img.paste(generate_item_row(item), (0, i*h))
    return img


images = []
for image in os.listdir("images"):
    images.append(Image.open(f"images/{image}"))

img = Image.new("RGB", (520, 86*len(images)+10), color = (27, 40, 56))
for i, image in enumerate(images):
    img.paste(image, (10, i*86+10))

img.show()
img.save("test.png")


