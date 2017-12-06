import discord
from discord.ext import commands

game = 0
djoueurs = 0
joueurs = str("0")

def is_joueurs(sender):
    global joueurs
    for i in range(len(joueurs)):
        if ctx == joueurs[i]:
            return True

        else:
            return False

class Garou:
    def __init__(self, bot):
        self.bot = bot


    #Commande de démarrage du Garou
    @commands.command(pass_context=True)
    async def gstart(self, ctx):
        """Démarrage d'une partie de Garou"""
        global game
        if game == 1:
            print("Commande gstart lancer par: "+str(ctx.message.author)+" refuser car une partie est deja en cours")
            await self.bot.say("Désoler mais une partie est deja en cours !")
        elif game == 0:
            game = 1
            gm = ctx.message.author
            print("L'ancement d'une partie de Garou par: "+str(ctx.message.author))
            await self.bot.say("Lancmeent d'une partie !")
            await self.bot.say("Veuiller specifier les joueurs avec la commande gjoueurs")

    #Commande pour definir les participant du Garou
    @commands.command(pass_context=True)
    async def gjoueurs(self, ctx, *, CMDjoueurs):
        global djoueurs
        global joueurs
        if game == 0:
            print("Commande gjoueurs lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")

        elif game == 1:
            if djoueurs == 1:
                print("Commande gjoueurs lancer par: "+str(ctx.message.author)+" refuser, partie deja lacer !")
                await slef.bot.say("Désoler mais une partie est deja en cours !")

            elif djoueurs == 0:
                djoueurs = 1
                joueurs = CMDjoueurs
                print("Commande gjoueurs lancer par: "+str(ctx.message.author)+" argument: "+str(CMDjoueurs))
                await self.bot.say("Les jouer de cette partie sont: "+str(joueurs))

    #Commande de test
    @commands.command(pass_content=True)
    async def gtest(self, ctx):
        sender = ctx.message.author
        if is_joueurs(sender) == True:
            await self.bot.say("Vous ete bien un joueurs !")

        elif gm == ctx.message.author:
            await self.bot.say("Vous ete le GM !")


        else:
            await self.bot.say("Vous n'ete pas un joueurs !")

    #Commande pour annuler le Garou
    @commands.command(pass_context=True)
    async def gstop(self, ctx):
        global game,djoueurs
        if game == 0:
            print("Commande gstop lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")

        elif game == 1:
            if gm == ctx.message.author:
                #reset de toutes les variables
                game = 0
                djoueurs = 0
                gm = 0
                print("Partie de garou annuler !")
                await self.bot.say("La partie de garou est annuler !")

            else:
                print("Commande gstop mancer par: "+str(ctx.message.author)+" refuser car ce n'est pas le gm !")
                await self.bot.say("Désoler mais vous n'avez pas le droit de faire ça, vous n'étes pas le gm !")


def setup(bot):
    bot.add_cog(Garou(bot))
