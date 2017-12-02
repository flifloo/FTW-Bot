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
        print("Commande ping lancer par: "+str(ctx.message.author))

    #Commande dis
    @commands.command(pass_context=True)
    async def dis(self, ctx, *, something):
        """Un mode peroquet"""
        await self.bot.say(something)
        print("Commande dis lancer par: "+str(ctx.message.author)+" argument: "+str(something))

    #Commande kick
    @commands.command(pass_context=True)
    async def kick(self, ctx, member:discord.Member):
        """Expulse un jouer"""
        #await self.bot.kick(member)
        await self.bot.say("Kick de: "+str(member)+" par: "+str(ctx.message.author))
        print("Commande kick lancer par: "+str(ctx.message.author)+" sur: "+str(member))

    #Commande flash
    @commands.command(pass_context=True)
    async def flash(self, ctx, *, something):
        """Fait apparaitre un text siblimiquement"""
        await self.bot.delete_message(ctx.message)
        print("Commande flash lancer par: "+str(ctx.message.author)+" argument: "+str(something))

    #Commande indirect
    @commands.command(pass_context=True)
    async def say(self, ctx, *, something):
        """Fait passer un message indirectement"""
        await self.bot.say("**{} said:** {}".format(str(ctx.message.author), something))
        await self.bot.delete_message(ctx.message)
        print("Commande say lancer par: "+str(ctx.message.author)+" argument: "+str(something))

    #Groupe de commande role
    @commands.group(pass_context=True)
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            """Permet la gestion de roles"""
            await self.bot.say("role: create; ...")
            print("Commande role lancer par: "+str(ctx.message.author))

    #Commande role create
    @role.command(pass_context=True)
    async def create(self, ctx, *, name):
        """Permer de crée un role"""
        await self.bot.say("Creation du role : "+str(name))
        print("Commande role create lancer par: "+str(ctx.message.author)+" argument: "+str(name))

    @commands.command(pass_context=True, aliases=["id"])
    async def ID(self, ctx):
            await self.bot.say("ID de l'envoyeur: "+ctx.message.author.id)
            print("Commande ID lancer par: "+str(ctx.message.author)+" résultat: "+str(ctx.message.author.id))
            
def setup(bot):
    bot.add_cog(DefaultCMD(bot))
