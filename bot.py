import json
import discord
from discord.ext import commands


with open('config.json') as json_data_file:
    parameter = json.load(json_data_file)

bot = commands.Bot(command_prefix=parameter['Bot']['prefix'], description=parameter['Bot']['description'])
bot.remove_command("help")


#Démarrage
@bot.event
async def on_ready():
    print("Définition du statut de base")
    await bot.change_presence(game=discord.Game(name=parameter['Bot']['statu']))

    print("Démarrage de DefaultCMD")
    bot.load_extension("DefaultCMD")

    print("Démarrage de Administration")
    bot.load_extension("Administration")

    print("Démarrage de Benne_a_ordure")
    bot.load_extension("Benne_a_ordure")

    print("Démarrage de Reactionner")
    bot.load_extension("Reactionner")

    print("Démarrage de Garou")
    bot.load_extension("Garou")

    print("Démarrage de Music")
    bot.load_extension("Music")

    print("FTW's Bot opérationel")
    embed=discord.Embed(title="Administration", description="", color=0xffff00)
    embed.set_thumbnail(url="https://icon-icons.com/icons2/562/PNG/512/on-off-power-button_icon-icons.com_53938.png")
    embed.add_field(name="Démarrage", value="FTW's Bot opérationel", inline=False)
    channel = bot.get_channel("389209382388498445")
    await bot.send_message(channel, embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    embed=discord.Embed(title="Music", description="Aide", color=0x80ff00)
    embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-help-128.png")
    embed.add_field(name="Bases", value="Pour voir les commandes basiques, écrivez: ```basic```", inline=True)
    embed.add_field(name="Garou", value="Pour voir les commandes du Garou, écrivez: ```lg help```", inline=True)
    embed.add_field(name="Music", value="Pour voir les commandes pour la musique, écrivez: ```music help```", inline=True)
    await bot.say(embed=embed)


bot.run(parameter['Bot']['token'])
