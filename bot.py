import json
import discord
from discord.ext import commands

with open('config.json') as json_data_file:
    parameter = json.load(json_data_file)

bot = commands.Bot(command_prefix=parameter['Bot']['prefix'], description=parameter['Bot']['description'])

owner = ["177393521051959306"]

def is_owner(id):
    for i in range(len(owner)):
        if id == owner[i]:
            return True
    return False

#Démarrage
@bot.event
async def on_ready():
    print("Démarrage de DefaultCMD")
    bot.load_extension("DefaultCMD")

    print("Démarrage de ExampleRepl")
    bot.load_extension("ExampleRepl")

    print("Démarrage de Benne_a_ordure")
    bot.load_extension("Benne_a_ordure")

    print("Démarrage de Reactionner")
    bot.load_extension("Reactionner")

    print("Démarrage de Garou")
    bot.load_extension("Garou")

    print("FTW's Bot operationelle")

@bot.command(pass_context = True)
async def load(ctx, ext):
    """: Charge une extension"""
    if is_owner(ctx.message.author.id) == True:
        bot.load_extension(ext)
        print("Extention "+str(ext)+" charger par: "+str(ctx.message.author))
        await bot.say("Extension "+str(ext)+" charger")
    else:
        await bot.say("Désoler <@"+str(ctx.message.author.id)+"> mais vous n'avez pas le droit de faire ca !")
        print("Refue de charger: "+str(ext)+" car "+str(ctx.message.author)+" n'a pas le droit !")

@bot.command(pass_context = True)
async def unload(ctx,ext):
    """: Décharge une extension"""
    if is_owner(ctx.message.author.id) == True:
        bot.unload_extension(ext)
        print("extention "+str(ext)+" décharger")
        await bot.say("Extension "+str(ext)+" décharger")
    else:
        await bot.say("Désoler <@"+str(ctx.message.author.id)+"> mais vous n'avez pas le droit de faire ca !")
        print("Refue de décharger: "+str(ext)+" car "+str(ctx.message.author)+" n'a pas le droit !")

@bot.command(pass_context = True)
async def reload(ctx,ext):
    """: Recharge une extension avec ses modifications"""
    if is_owner(ctx.message.author.id) == True:
        bot.unload_extension(ext)
        bot.load_extension(ext)
        print("Extention "+str(ext)+" mis à jour par: "+str(ctx.message.author))
        await bot.say("Extension "+str(ext)+" mis à jour")
    else:
        await bot.say("Désoler <@"+str(ctx.message.author.id)+"> mais vous n'avez pas le droit de faire ca !")
        print("Refue de mettre à jour: "+str(ext)+" car "+str(ctx.message.author)+" n'a pas le droit !")

"""
@bot.event
async def on_message(msg):
    print(msg.content)
"""

bot.run(parameter['Bot']['token'])
