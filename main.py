import os
import json
import discord
from discord.ext import commands

# Načítanie tokenu zo systémovej premennej
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents musia obsahovať message_content
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Načítanie zostatkov zo súboru (ak existuje)
if os.path.exists("balances.json"):
    with open("balances.json", "r") as f:
        balances = json.load(f)
else:
    balances = {}

# Funkcia na uloženie zostatkov
def save_balances():
    with open("balances.json", "w") as f:
        json.dump(balances, f)

@bot.event
async def on_ready():
    print(f"{bot.user} je prihlásený a pripravený!")

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    balance = balances.get(user_id, 0)
    await ctx.send(f"Tvoj zostatok je {balance} Gold.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setbalance(ctx, member: discord.Member, amount: int):
    balances[str(member.id)] = amount
    save_balances()
    await ctx.send(f"Nastavil som {member.mention} zostatok na {amount} Gold.")

@bot.command()
@commands.has_permissions(administrator=True)
async def addbalance(ctx, member: discord.Member, amount: int):
    user_id = str(member.id)
    balances[user_id] = balances.get(user_id, 0) + amount
    save_balances()
    await ctx.send(f"Pridal som {amount} Gold {member.mention}. Nový zostatok: {balances[user_id]} Gold.")

@bot.command()
@commands.has_permissions(administrator=True)
async def removebalance(ctx, member: discord.Member, amount: int):
    user_id = str(member.id)
    balances[user_id] = max(balances.get(user_id, 0) - amount, 0)
    save_balances()
    await ctx.send(f"Odobral som {amount} Gold {member.mention}. Nový zostatok: {balances[user_id]} Gold.")

# Spustenie bota
bot.run(TOKEN)
