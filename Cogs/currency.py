import random, json
import discord
from discord.ext import commands

import curHelper as func


class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.coin = '<:TrollCoin:928330878155898910>'

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        new = await func.create_acc(ctx.author)
        users = await func.get_bank_data()
        wallet_bal = users[str(ctx.author.id)]["wallet"]
        bank_bal = users[str(ctx.author.id)]["bank"]

        embed = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.light_grey())
        embed.add_field(name="Wallet balance", value = f'{self.coin} {wallet_bal}')
        embed.add_field(name="Bank balance", value = f'{self.coin} {bank_bal}')

        if new:
            await ctx.send(f"Your TrollBank account has been registered!\nReceived {self.coin}**500** for Registration", embed = embed)

        else:
            await ctx.send(embed = embed)

    @commands.command()
    async def steal(self, ctx, user = None):
        try:
            user = self.client.get_user(user.replace(' ', '')[3, -1])
            await ctx.send(f"{user}\nYo your code works!")
            return
        except:
            await ctx.send("You gotta mention someone")
            return
        
        await func.create_acc(ctx.author)
        users = await func.get_bank_data()

        if random.randint(0, 1) == 0:
            money = random.randint(10, 500)
            await func.bank_update(ctx.author, money)
            await ctx.send(f"You successfully stole {self.coin}**{money}**!")
        else:
            if random.randint(0, 3) == 0:
                await ctx.send("You got caught but managed to escape!")
            else:
                if users[str(ctx.author.id)]["wallet"] != 0:
                    money = random.randint(int(users[str(ctx.author.id)]["wallet"]/10), int(users[str(ctx.author.id)]["wallet"]/2))
                    await func.bank_update(ctx.author, -money)

                    await ctx.send(f"You were caught! You paid the victim {self.coin}**{money}**.")
                else:
                    await ctx.send("You got caught but managed to escape!")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount = None):
        await func.create_acc(ctx.author)
        users = await func.get_bank_data()

        if amount.lower() == 'all':
            await func.bank_update(ctx.author, users[str(ctx.author.id)]["bank"])
            await func.bank_update(ctx.author, -users[str(ctx.author.id)]["bank"], "bank")
            await ctx.send(f'Withdrew {self.coin}**{str(users[str(ctx.author.id)]["bank"])}**.')
            return

        if amount == None:
            await ctx.send("You didn't specify the amount to withdraw.")
            return

        try:
            amount = int(amount)
        except:
            await ctx.send("Please enter a valid amount")
            return

        if int(users[str(ctx.author.id)]["bank"]) < amount:
            await ctx.send("You don't have that much money LOL")
            return

        await func.bank_update(ctx.author, amount)
        await func.bank_update(ctx.author, -amount, "bank")
        await ctx.send(f"Withdrew {self.coin}**{amount}**.")

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount = None):
        await func.create_acc(ctx.author)
        users = await func.get_bank_data()

        if amount.lower() == 'all':
            await func.bank_update(ctx.author, users[str(ctx.author.id)]["wallet"], "bank")
            await func.bank_update(ctx.author, -users[str(ctx.author.id)]["wallet"])
            await ctx.send(f'Deposited {self.coin}**{str(users[str(ctx.author.id)]["wallet"])}**.')
            return

        if amount == None:
            await ctx.send("You didn't specify the amount to deposit.")
            return

        try:
            amount = int(amount)
        except:
            await ctx.send("Please enter a valid amount")
            return

        if int(users[str(ctx.author.id)]["wallet"]) < amount:
            await ctx.send("You don't have that much money LOL")
            return

        await func.bank_update(ctx.author, amount, "bank")
        await func.bank_update(ctx.author, -amount)
        await ctx.send(f"Deposited {self.coin}**{amount}**.")

    @commands.command()
    async def shop(self, ctx, item=None):
        if item == None:
            embed = await func.get_shop()
            await ctx.send(embed=embed)
        else:
            embed = await func.get_item(item)
            if embed == 1:
                await ctx.send("Item not found in the shop.")
                return
            await ctx.send(embed=embed)

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, user : discord.Member = None):
        async with ctx.typing():
            if user == None:
                user = ctx.author

            await func.create_inv(user)
            inv_data = await func.get_inv_data()

            with open("shop.json", "r") as shop:
                shop = json.load(shop)

            embed = discord.Embed(title=f"{user.name}'s Inventory", color=discord.Color.light_grey())
            for obj in inv_data[str(user.id)]:
                for i in shop:
                    if shop[i]["id"] == obj:
                        embed.add_field(name=f"{shop[i]['icon']} {shop[i]['name']}", value=f"**{inv_data[str(user.id)][obj]}** owned", inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Currency(client))
