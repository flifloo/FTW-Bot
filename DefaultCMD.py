import discord
from discord.ext import commands

class DefaultCMD:
    def __init__(self, bot):
        self.bot = bot

    #Commande ping
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """La commande la plus stupide de se bot"""
        await self.bot.say("Pong!")
        print("Commande ping lancée par: "+str(ctx.message.author))

    #Commande dis
    @commands.command(pass_context=True)
    async def dis(self, ctx, *, something):
        """Un mode peroquet"""
        await self.bot.say(something)
        print("Commande dis lancée par: "+str(ctx.message.author)+" argument: "+str(something))

    #Commande flash
    @commands.command(pass_context=True)
    async def flash(self, ctx, *, something):
        """Fait apparaitre un text siblimiquement"""
        await self.bot.delete_message(ctx.message)
        print("Commande flash lancée par: "+str(ctx.message.author)+" argument: "+str(something))

    #Commande indirect
    @commands.command(pass_context=True)
    async def say(self, ctx, *, something):
        """Fait passer un message indirectement"""
        await self.bot.say("**{} said:** {}".format(str(ctx.message.author), something))
        await self.bot.delete_message(ctx.message)
        print("Commande say lancée par: "+str(ctx.message.author)+" argument: "+str(something))



def setup(bot):
    bot.add_cog(DefaultCMD(bot))
    print("DefaultCMD chargée")
