# client Mahmoud

import discord
from urllib.request import 	urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import itertools
import csv
import random
from config_bot import *

# TODO &help
# TODO &m help 
# TODO Que se passe t il quand on lance plusieurs &p à la fois ?
# TODO clear @user number
# TODO search yt


PREFIX = Config.PREFIX
TOKEN = Config.TOKEN
DELETE_AFTER = 10


client = commands.Bot(command_prefix=PREFIX)

@client.event
async def on_ready():
    print ("I am running on " + client.user.name)
    print ("With the ID: " + client.user.id)
    await client.change_presence(game=discord.Game(name=' la dinette'))


@client.command(pass_context=True)
async def hello(ctx):
    await client.say("Va bien niquer ta mère fdp !")


@client.command(pass_context=True)
async def info(ctx, user : discord.Member):
    embed = discord.Embed(title = "Informations sur {}".format(user.name), description = "Voilà ce que j'ai pu trouver.",color =0x00ff00)
    embed.add_field(name="Pseudo", value=user.name, inline = True)
    embed.add_field(name="ID", value=user.id,inline=True)
    embed.add_field(name="Rôle", value=user.top_role)
    embed.add_field(name="Date d'arrivée",value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

@client.command(pass_context=True, aliases=['serverinfo', 'server', 'serveri'])
@commands.has_role("Con de service" or "Chieuse de service" or "Macaque")
async def sinfo(ctx):
    embed = discord.Embed(name="Informations sur le serveur {}".format(ctx.message.server.name), description = "Voilà ce que j'ai pu trouver.", color = 0x00ff00)
    embed.set_author(name="")
    embed.add_field(name="Pseudo", value=ctx.message.server.name, inline = True)
    embed.add_field(name="ID", value=ctx.message.server.id,inline=True)
    embed.add_field(name="Rôles", value="Il y a {} rôles".format(len(ctx.message.server.roles)))
    embed.add_field(name="Membres",value="Il y a {} utilisateurs".format(len(ctx.message.server.members)))
    embed.set_thumbnail(url=ctx.message.server.icon_url)

    await client.say(embed=embed, delete_after = DELETE_AFTER)

# clear : Pour supprimer tous les messages du channel // TODO @author 

@client.command(pass_context = True, aliases=['clea', 'cle', 'cl', 'c'])
async def clear(ctx, number = 1, author : discord.Member = None):
    messages = []
    number = int(number)
    async for message in client.logs_from(ctx.message.channel, limit = number + 1):
        if (author is None):
            messages.append(message)
        else:
            if message.author == author:
                messages.append(message)
    await client.delete_messages(messages)




#m 
file = open("content/memes.txt")
memes_array = []
for line in file.readlines():
    y = [value for value in line.strip().split('\t')]
    memes_array.append(y)


file.close()

@client.command(pass_context=True, aliases=['meme', 'mem', 'me'])
async def m(ctx, arg):

    url=''
    m_commands=[]
    output =[]
    
    for meme in memes_array:
        m_commands.append(meme[1])
        if(meme[1] == arg):
            url = meme[0]
    
    if (arg == 'help'):
        embed = discord.Embed(title = "Commandes memes help :", description = "Aide sur les commandes de memes",color =0x00ff00)
        for m_command in m_commands:
             output.append(PREFIX + "m " + str(m_command))

        com_str = '\n'.join(str(e) for e in output)
        embed.add_field(name= PREFIX + "m help", value=com_str, inline = True)
        await client.say(embed=embed)

    elif  not url=='':

        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await client.say("Tu n'es pas dans un channel connard !")
            return False

        if not client.is_voice_connected(ctx.message.server):
            vc = await client.join_voice_channel(summoned_channel)
        else:
            vc = client.voice_client_in(ctx.message.server)

        player = await vc.create_ytdl_player(url)
        player.volume = 0.3
        player.start()
    
    else:
        await client.say("Commande inconnue.", delete_after = DELETE_AFTER)

    await client.delete_message(ctx.message)


@client.command(pass_context=True, aliases=['play', 'pl', 'pla'])
async def p(ctx, url):

    summoned_channel = ctx.message.author.voice_channel
    if summoned_channel is None:
        await client.say("Tu n'es pas dans un channel connard !")
        return False

    if not client.is_voice_connected(ctx.message.server):
        vc = await client.join_voice_channel(summoned_channel)
    else:
        vc = client.voice_client_in(ctx.message.server)

    player = await vc.create_ytdl_player(url)
    player.volume = 0.1
    player.start()

    await asyncio.sleep(60)
    await client.delete_message(ctx.message)




@client.command(pass_context=True, aliases=['degag', 'dega', 'deg', 'd'])
async def degage(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client:
        await voice_client.disconnect()
        print("J'me tire !")
    else:
        print("J'étais même pas là connard")
    
    #await client.delete_message(ctx.message)


#m 
file = open("content/category.txt")
category_array = []
for line in file.readlines():
    y = [value for value in line.strip().split('\t')]
    category_array.append(y)


file.close()

@client.command(pass_context=True, aliases=['cat'])
async def category(ctx,arg = None):

    category_matching = []
    if arg is None:
        cat_chosen = random.choice(category_array)
    
    else:        
        for category in category_array:
            if str(arg) in category[0]:
                category_matching.append(category)
        if not category_matching:
            await client.say("J'ai rien trouvé avec tes mots clés de merde.", delete_after = DELETE_AFTER)
            await asyncio.sleep(10)
            await client.delete_message(ctx.message)
        
    
        cat_chosen = random.choice(category_matching)
    
    cat_chosen_str = '\n'.join(str(e) for e in cat_chosen)

    url_p = Config.URL_P
    url_f = url_p + '/search/' + cat_chosen_str

    r = requests.get(url_f)

    page_soup = soup(r.content, "html.parser")
    elements = page_soup.findAll("ul",{"class":"thumbs container"})[0]
    element = elements.findAll("li",{"class":"thumb sub"})[0]
    sub_link = element.div.find("a",{"class":"item-link"})['href']
    link = url_p + sub_link
    title = element.div.find("a",{"class":"item-link"})['title']
    site_p = element.div.findAll("span",{"class":"source"})[0].a.findAll(text=True)[0]
    
    embed = discord.Embed(name="Résultats : ", color = 0x00ff00)
    embed.add_field(name="Catégorie",value="["+str(cat_chosen_str)+"]"+"("+str(link)+")")
    embed.add_field(name='Site',value=str(site_p))
    embed.add_field(name='Titre',value=str(title))
    embed.set_thumbnail(url='https://ih1.redbubble.net/image.113815690.9530/flat,550x550,075,f.u4.jpg')

    await client.say(embed=embed, delete_after= DELETE_AFTER)
    await asyncio.sleep(10)
    await client.delete_message(ctx.message)
    

    

client.run(TOKEN)
