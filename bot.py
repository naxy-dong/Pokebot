import os # operating system
import discord # discord package
from discord.ext import commands 
import requests

description = ''' Help command Discription '''
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", description=description, intents=intents) # discord bot initialization

# make the bot print something out when it goes online
@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

# make the bot print something out when someone sends a text
@bot.event
async def on_message(message):
    if not message.author == bot.user:
        print('Message from {0.author}: {0.content}'.format(message))
    await bot.process_commands(message)

# make the bot send to chat when someone requests info for a pokemon
@bot.command()
async def info(ctx, arg, *options):

    #STEP 1: get info from user and set into variables and make data request
    pokeball_url = 'https://cdn-icons-png.flaticon.com/512/419/419467.png'
    pokemon = arg.lower()
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}') # request info about pokemon
    
    data = r.json()

    r2 = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon}') # request info about pokedex entry
    data2 = r2.json()

    # Step 2: take our data and parse into vars for future use
    name = data["name"] # name of pokemon
    sprite = data["sprites"]["front_default"] # pokemon sprite
    official_image = data["sprites"]["other"]["official-artwork"]["front_default"] # offical_art_work
    stats = data["stats"] # array of stats 
    flavor_text_entries = data2["flavor_text_entries"] # pokedex entry

    def find_first_en():
        for flavor in flavor_text_entries:
            if flavor['language']['name'] == 'en':
                return flavor


    pkmn_stats = f"HP: {stats[0]['base_stat']}\n" \
                 f"Attack: {stats[1]['base_stat']}\n" \
                 f"Defense: {stats[2]['base_stat']}\n" \
                 f"Special-Attack: {stats[3]['base_stat']}\n" \
                 f"Special-Defense: {stats[4]['base_stat']}\n" \
                 f"Speed: {stats[5]['base_stat']}" # add speed stats


    # step 3: create embed object creation and initialization
    embed = discord.Embed(title=f"{name.upper()}", color=discord.Color.from_rgb(204, 0, 0)) # add title and color
    embed.add_field(name='About', value=find_first_en()['flavor_text'])
    embed.add_field(name='Stats', value=pkmn_stats, inline=False)

    # add options abilities, types, and/or shiny optons
    for option in options:
        if option.lower() == 'abilities': # abilities
            abilities = data['abilities']
            temp = ''
            for ability in abilities[:-1]:
                temp += f" {ability['ability']['name']},"
            temp += f" {abilities[-1]['ability']['name']}."
            embed.add_field(name="Abilities", value=temp, inline=True)
            embed.add_field(name='\u200b', value= '\u200b')
        elif option == 'types': # types
            types = data['types']
            temp = ''
            for family in types[:-1]:
                temp += f" {family['type']['name']},"
            temp += f" {types[-1]['type']['name']}."
            embed.add_field(name="Types", value=temp, inline=True)
            embed.add_field(name='\u200b', value= '\u200b')
        elif option.lower() == 'shiny': # shiny
            sprite = data['sprites']['front_shiny']


    # finish off with image
    embed.set_image(url=official_image) # add offical pkmn images
    embed.set_footer(text=f'{name}', icon_url=pokeball_url)# create a footer with pokeball and name
    embed.set_thumbnail(url=sprite) # set a thumbnail for our embed

    # step 4: send embed to server
    await ctx.send(embed=embed) 

bot.run("NzIyOTgwNjgzODY1MjYwMDU0.Gj5_27.eNwc7UymGlD2xGF-nYptQ46Rar5bGYEhL--Ud0")