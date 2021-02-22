import discord
from discord.ext import commands
import json


## getting data to start the bot

# getting the prefix
def get_prefix():
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['prefix']


# getting the bot's token
def get_token():
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['token']
        


# creating the bot
bot = commands.Bot(command_prefix = get_prefix())



# getting the set price of a single dash
def get_price():
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['price']


# setting the price of a single dash
def set_price(new_price):
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['price'] = new_price

    with open('vonal.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


# incrementing the score of a member 
# member must have the given main_name in json file
# member must be in json file
def add_lines(main_name, count):
    prev_score = -1
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for p in data['people']:
            if p['name'] == main_name:
                prev_score = p['score']
                p['score'] = prev_score + count
                break
        if prev_score == -1:
            print('Who is dat?')

    with open('vonal.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent = 4)


# matching a main_name to the given (alias) name
def get_main_name(name):
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for p in data['people']:
            for alias in p['aliases']:
                if alias == name.lower():
                    return p['name']
    return None


# getting the people from json
def get_people():
    with open('vonal.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['people']




## events and command handling


# at starting up
@bot.event
async def on_ready():
    s = discord.Status.online
    a = discord.Game("Counting dashes")
    await bot.change_presence(status=s, activity=a)
    print('VoNaL logged in')


# for testing
@bot.command(help = 'Sends a pong message')
async def ping(ctx):
    await ctx.send('Pong?')


# getting bot to go offline
@bot.command(aliases = ['49', 'leave', 'go'], help = 'This makes VoNaL go offline :(')
@commands.has_any_role('szobapatrióta', 'admin')
async def quit(ctx):
    await ctx.send('See you soon!')
    await bot.change_presence(status=discord.Status.offline)
    # Note that VoNaL doesn't actually leave the server


# setting command (sets the price of a single dash)
@bot.command(help = 'Sets the price for a single dash')
async def setprice(ctx, price : int):
    if price > 0:
        set_price(price)
    await ctx.send(f'The new price of a swear is {get_price()}')


# adding [count] number of dashes to the score of the given member(s)
@bot.command(aliases = [''], help = '`| 3 @Martin` adds 3 dashes to Martin')
async def add(ctx, count = 1, *members : discord.Member):

    if count > 0:

        for m in members:
            main_name = get_main_name(m.name)
            if main_name != None:
                add_lines(main_name, count)

        if len(members) > 0:
            mentionstring = ''
            for m in members:
                mentionstring = mentionstring + f'{m.mention} '
            await ctx.send(f'I added {count} | to {mentionstring}')
        else:
            main_name = get_main_name(ctx.author.name)
            add_lines(main_name, count)
            await ctx.send(f'I added {count} | to {ctx.author.mention}')


# increments score of sender
@bot.command(aliases = ['++'], help = 'Increments your score')
async def inc(ctx):

    main_name = get_main_name(ctx.author.name)
    add_lines(main_name, 1)
    await ctx.send(f'I added a | to {ctx.author.mention}')


# adds [count] number of dashes to the score of the sender
@bot.command(aliases = ['+='], help = 'Adds the given number of dashes to your score')
async def incmany(ctx, count : int):

    if count > 0:
        main_name = get_main_name(ctx.author.name)
        add_lines(main_name, count)
        await ctx.send(f'I added {count} | to {ctx.author.mention}')


# displaying current score
@bot.command(help = 'Displays the current score')
async def score(ctx):
    disp = ''
    people = get_people()
    for p in people:
        name = p['name']
        disp += f'{name}:\n'
        cnt = p['score']
        disp += (cnt // 5) * ('~~||||~~ ')
        disp += (cnt %  5) * '\|'
        disp += f'\t{get_price()*cnt}.-\n'

    await ctx.send(disp)


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if not msg.content.startswith(get_prefix()):
        return
    
    await bot.process_commands(msg)
    await msg.delete()


bot.run(get_token())

#TODO help (for all commands)

#TODO CommandNotFound, MissingPermissions