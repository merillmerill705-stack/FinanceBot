import os
import discord
from discord.ext import commands

TOKEN = os.getenv("MTQwNjUzOTYxODk3OTE1MTkxMw.GjTD84.fXFfI0qhO-n4oLjYDFqYdzhLKrs6N_igEhaGR8")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

# databáza – zatiaľ jednoduchý slovník
balances = {}

@bot.event
async def on_ready():
    print(f"{bot.user} je prihlásený a pripravený!")

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    balance = balances.get(user_id, 0)
    await ctx.send(f"Tvoj zostatok je {balance}€.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setbalance(ctx, member: discord.Member, amount: int):
    balances[str(member.id)] = amount
    await ctx.send(f"Nastavil som {member.mention} zostatok na {amount}Gold.")

bot.run(MTQwNjUzOTYxODk3OTE1MTkxMw.GjTD84.fXFfI0qhO-n4oLjYDFqYdzhLKrs6N_igEhaGR8)
