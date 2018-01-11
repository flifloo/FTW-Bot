import json
import discord
from discord.ext import commands


class Administration:
    def __init__(self, bot):
        self.bot = bot

    with open('config.json') as json_data_file:
        parameter = json.load(json_data_file)

    owner = parameter['Perms']['Admin']

    def is_owner(self, id):
        for i in range(len(self.owner)):
            if id == self.owner[i]:
                return True
        return False


    #Gestion des extension
    @commands.group(pass_context=True)
    async def extension(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.help)

    #Help des extension
    @extension.command(pass_context=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Extension", description="Aide", color=0xff0000)
        embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
        embed.add_field(name="load", value="Charge une extension", inline=True)
        embed.add_field(name="unload", value="Décharge une extension", inline=True)
        embed.add_field(name="reload", value="Recharge une extension", inline=True)
        await self.bot.say(embed=embed)

    #Charger une extension
    @extension.command(pass_context=True)
    async def load(self, ctx, ext):
        if self.is_owner(ctx.message.author.id) == True:
            self.bot.load_extension(ext)
            print("Extention "+str(ext)+" charger par: "+str(ctx.message.author))
            embed=discord.Embed(title="Administration", description="Modules", color=0xffff00)
            embed.add_field(name="Chargement", value="Extension "+str(ext)+" charger", inline=False)
            await self.bot.say(embed=embed)

        else:
            print("Refue de charger: "+str(ext)+" car "+str(ctx.message.author)+" n'a pas le droit !")
            embed=discord.Embed(title="Administration", description="Modules", color=0xffff00)
            embed.add_field(name="Chargement", value="Désoler <@"+str(ctx.message.author.id)+"> mais vous n'avez pas le droit de faire ca !", inline=False)
            await self.bot.say(embed=embed)

    #Décharger une extension
    @extension.command(pass_context=True)
    async def unload(self, ctx, ext):
        if self.is_owner(ctx.message.author.id) == True:
            self.bot.unload_extension(ext)
            print("extention "+str(ext)+" décharger")
            embed=discord.Embed(title="Administration", description="Modules", color=0xffff00)
            embed.add_field(name="Déchargement", value="Extension "+str(ext)+" décharger", inline=False)
            await self.bot.say(embed=embed)

        else:
            print("Refue de décharger: "+str(ext)+" car "+str(ctx.message.author)+" n'a pas le droit !")
            embed=discord.Embed(title="Administration", description="Modules", color=0xffff00)
            embed.add_field(name="Déchargement", value="Désoler <@"+str(ctx.message.author.id)+"> mais vous n'avez pas le droit de faire ca !", inline=False)
            await self.bot.say(embed=embed)

    #Recharger une extension
    @extension.command(pass_context=True)
    async def reload(self, ctx, ext):
        if self.is_owner(ctx.message.author.id) == True:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
            print("Extention "+str(ext)+" mis à jour par: "+str(ctx.message.author))
            embed=discord.Embed(title="Administration", description="Modules", color=0xffff00)
            embed.add_field(name="Reload", value="Extension "+str(ext)+" mis à jour", inline=False)
            await self.bot.say(embed=embed)

        else:
            print("Refue de mettre à jour: "+str(ext)+" car "+str(ctx.message.author)+" n'a pas le droit !")
            embed=discord.Embed(title="Administration", description="Modules", color=0xffff00)
            embed.add_field(name="Reload", value="Désoler <@"+str(ctx.message.author.id)+"> mais vous n'avez pas le droit de faire ca !", inline=False)
            await self.bot.say(embed=embed)


    #Eteindre le bot
    @commands.command(pass_context=True)
    async def shutdown(self, ctx):
        if self.is_owner(ctx.message.author.id) == True:
            print("Arret du bot fait par:"+str(ctx.message.author)+" !")
            embed=discord.Embed(title="Administration", description="", color=0xffff00)
            embed.set_thumbnail(url="https://icon-icons.com/icons2/562/PNG/512/on-off-power-button_icon-icons.com_53938.png")
            embed.add_field(name="Arret", value="FTW's Bot arréter", inline=False)
            await self.bot.say(embed=embed)
            await self.bot.logout()
            await self.bot.close()

        else:
            print("Arret du bot fait par:"+str(ctx.message.author)+" refuser")
            embed=discord.Embed(title="Administration", description="", color=0xffff00)
            embed.set_thumbnail(url="https://icon-icons.com/icons2/562/PNG/512/on-off-power-button_icon-icons.com_53938.png")
            embed.add_field(name="Erreur", value="Désoler mais vous n'avez pas le droit !", inline=False)
            await self.bot.say(embed=embed)
            await self.bot.logout()
            await self.bot.close()


def setup(bot):
    bot.add_cog(Administration(bot))
    print("Administration charger")
