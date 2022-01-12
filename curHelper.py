import json
import discord

coin = '<:TrollCoin:928330878155898910>'

async def get_shop():
    with open("shop.json", "r") as shop:
        shop = json.load(shop)
        embed = discord.Embed(title="Troll Shop", color=discord.Colour.light_grey())
        for item in shop:
            if shop[item]["price"] == 0:
                embed.add_field(name=f'{shop[item]["icon"]} {shop[item]["name"]}', value=f'cannot be purchased', inline=False)
            else:
                embed.add_field(name=f'{shop[item]["icon"]} {shop[item]["name"]}', value=f'1 for {coin}**{shop[item]["price"]}**', inline=False)

    return embed

async def get_item(user_item):
    with open("shop.json", "r") as shop:
        shop = json.load(shop)
        for item in shop:
            if shop[item]["id"] == user_item.lower():
                price = str(shop[item]["price"])
                sell = str(shop[item]["sell"])
                if price == '0':
                    price = '`unavailable`'
                else:
                    price = coin + price
                
                if sell == '0':
                    sell = '`unavailable`'
                else:
                    sell = coin + sell
                
                embed = discord.Embed(title=shop[item]["name"], description=shop[item]["description"], color=discord.Color.light_grey())
                thumbnail = f'https://cdn.discordapp.com/emojis/{(shop[item]["icon"][-19:-1])}.png?size=128&quality=lossless'
                embed.set_thumbnail(url=thumbnail)
                embed.add_field(name="SHOP", value=f"**Buying Price :** {price}\n**Selling Price :** {sell}", inline=False)
                embed.add_field(name="ID", value=f"`{shop[item]['id']}`", inline=False)
                return embed
    return 1

async def create_acc(user):
    users = await get_bank_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 500

    with open("bank.json", "w") as f:
        json.dump(users, f, indent=4)
    return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users

async def bank_update(user, change, mode="wallet"):
    await create_acc(user)
    users = await get_bank_data()
    
    users[str(user.id)][mode] += change

    with open("bank.json", "w") as f:
        json.dump(users, f, indent=4)

async def create_inv(user):
    users = await get_inv_data()
    if str(user.id) in users:
        return
    else:
        users[str(user.id)] = {}

    with open("inv.json", "w") as f:
        json.dump(users, f, indent=4)
    return

async def get_inv_data():
    with open("inv.json", "r") as f:
        users = json.load(f)
    return(users)

async def inv_update(user, item, amt):
    await create_inv(user)
    users = await get_inv_data()
    users_bank = await get_bank_data

    if amt*item["price"] > users_bank[str(user.id)]["wallet"]:
        return 1

    with open("shop.json", "r") as shop:
        shop = json.load(shop)

    for i in shop:
        if shop[i]["name"] == item["name"]:
            for obj in users[str(user.id)]:
                if obj == item["name"]:
                    users[str(user.id)][obj] += amt
                    await bank_update(user, -amt*item["price"])
                    return
            users[str(user.id)] = {}
            users[str(user.id)][obj] += amt
            await bank_update(user, -amt*item["price"])
            return

    return 2