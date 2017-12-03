import discord
from discord.ext import commands

game = 0
djouers = 0

class Garou:
    def __init__(self, bot):
        self.bot = bot

    #Commande de démarrage du Garou
    @commands.command(pass_context=True)
    async def gstart(self, ctx):
        """Démarrage d'une partie de Garou"""
        if game == 1:
            print("Commande gstart lancer par: "+str(ctx.message.author)+" refuser car une partie est deja en cours")
            await self.bot.say("Désoler mais une partie est deja en cours !")
        elif game == 0:
            game = 1
            gm = ctx.message.author
            print("L'ancement d'une partie de Garou par: "+str(ctx.message.author))
            await self.bot.say("Lancmeent d'une partie !")
            await self.bot.say("Veuiller specifier les joueurs avec la commande gjouers")
    
    #Commande pour definir les participant du Garou
    @commands.command(pass_context=True)
    async def gjouers(self, ctx, *, jouers):
        if game == 0:
            print("Commande gjouers lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")
        
        elif game == 1:
            if djouers == 1:
                print("Commande gjouers lancer par: "+str(ctx.message.author)+" refuser, partie deja lacer !")
                await slef.bot.say("Désoler mais une partie est deja en cours !")
            
            elif djouers == 0:
                djouers = 1
                print("Commande gjouers lancer par: "+str(ctx.message.author)+" argument: "+str(jouers))
                await self.bot.say("Les jouer de cette partie sont: "+str(jouers))
    
    
    #Commande pour annuler le Garou
    @commands.command(pass_context=True)
    async def gstop(self, ctx):
        if game == 0:
            print("Commande gstop lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")
        
        elif game == 1:
            if gm == ctx.message.author:
                #reset de toutes les variables
                gam = 0
                djouers = 0
                gm = 0
                print("Partie de garou annuler !")
                await self.bot.say("La partie de garou est annuler !")
                
            else:
                print("Commande gstop mancer par: "+str(ctx.message.author)+" refuser car ce n'est pas le gm !")
                await self.bot.say("Désoler mais vous n'avez pas le droit de faire ça, vous n'étes pas le gm !")
            

def setup(bot):
    bot.add_cog(Garou(bot))