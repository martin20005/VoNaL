import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '|')
TOKEN = 'NzkxMzI5Mjc4ODgwMTIwODMy.X-Nk0g.E3ACxpYGqEQhxc15EClKCNCB988'
#TODO hide token

pricePerSwear = 20

@bot.event
async def on_ready():
    s = discord.Status.online
    a = discord.Game("Counting lines")
    await bot.change_presence(status=s, activity=a)
    print('VoNaL logged in')
    #TODO Read data (current price, counting, (token?))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong?')

@bot.command(aliases = ['49', 'leave', 'go'], help = 'This makes VoNaL leave :(')
@commands.has_any_role('szobapatrióta', 'admin')
async def quit(ctx):
    await ctx.send('See you soon!')
    await bot.change_presence(status=discord.Status.offline)
    print('VoNaL left')
    # Note that VoNaL doesn't actually leave the server

@bot.command()
async def setprice(ctx, price=20):
    pricePerSwear = price
    await ctx.send(f'The new price of a swear is {pricePerSwear}')

@bot.command(aliases = ['', '+'])
async def add(ctx):
    await ctx.send('I tried adding a |')
    #TODO add a | to sender



bot.run(TOKEN)

#TODO help (for all commands)
#TODO |score
#TODO | @member
#TODO | [number of new lines]
#TODO ||| 

#TODO CommandNotFound, MissingPermissions
#TODO magyarul