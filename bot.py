import discord
from discord.ext import commands
import json




# getting data from vonal.json
 
def get_prefix():
    with open('vonal.json', 'r') as f:
        data = json.load(f)
        return data['prefix']

def get_token():
    with open('vonal.json', 'r') as f:
        data = json.load(f)
        return data['token']
        
bot = commands.Bot(command_prefix = get_prefix())
TOKEN = get_token()

def get_price():
    with open('vonal.json', 'r') as f:
        data = json.load(f)
        return data['price']

def set_price(new_price):
    with open('vonal.json', 'r') as f:
        data = json.load(f)

    data['price'] = new_price

    with open('vonal.json', 'w') as f:
        json.dump(data, f, indent=4)


def add_lines(main_name, count):
    prev_score = -1
    with open('vonal.json', 'r') as f:
        data = json.load(f)
        for p in data['people']:
            if p['name'] == main_name:
                prev_score = p['score']
                p['score'] = prev_score + count
                break
        if prev_score == -1:
            print('Who is dat?')

    with open('vonal.json', 'w') as f:
        json.dump(data, f, indent = 4)

def get_main_name(name):
    with open('vonal.json', 'r') as f:
        data = json.load(f)
        for p in data['people']:
            for alias in p['aliases']:
                if alias == name.lower():
                    return p['name']





# events and command handling

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
    # Note that VoNaL doesn't actually leave the server

@bot.command()
async def setprice(ctx, price=20):
    if price > 0:
        set_price(price)
    await ctx.send(f'The new price of a swear is {get_price()}')

@bot.command(aliases = ['', '+'])
async def add(ctx, *, msg):
    count = 0
    for word in msg:
        for ch in word:
            if ch == '|':
                count += 1
    real_name = get_main_name(ctx.author.name)
    add_lines(real_name, count)

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