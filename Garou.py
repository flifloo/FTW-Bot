import discord
import random
from discord.ext import commands

#Variables de base
game = 0
djoueurs = 0
gm = str()
joueurs = list()

#Vrai variables
minijoueurs = 5 #Le nombre minimum de joueurs qu'il faut pour lancer une partie
roles = ["", ""] #Les roles donner


def is_joueurs(target):
    global joueurs
    for i in range(len(joueurs)):
        if target == joueurs[i]:
            return True
    return False


class Garou:
    def __init__(self, bot):
        self.bot = bot

    #Définition du groupe de commande lg
    @commands.group(pass_context=True)
    async def lg(self, ctx):
        if ctx.invoked_subcommand is None:
            # do something that should only happen if no subcommands are called
            await self.bot.say("Jeux garou : start, joueurs, stop")

    #Commande pour démarre le jeux
    @lg.command(pass_context=True)
    async def start(self, ctx):
        global game,gm
        if game == 1:
            print("Commande lg start lancer par: "+str(ctx.message.author)+" refuser, partie deja lancer")
            await self.bot.say("Désoler mais une partie est deja en cours !")

        elif game == 0:
            game=1
            gm=ctx.message.author
            print("Commande lg start lancer par "+str(ctx.message.author))
            #await self.bot.say("Lancement de la partie !")
            await self.bot.say("Veuiller specifier les participants avec la commande: ```lg joueurs```.")

    #Commande pour definir les participant du Garou
    @lg.command(pass_context=True)
    async def joueurs(self, ctx):
        global djoueurs,joueurs,gm
        if game == 0:
            print("Commande lg joueurs lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")

        elif game == 1:
            if djoueurs >= 1:
                print("Commande lg joueurs lancer par: "+str(ctx.message.author)+" refuser, partie deja lacer !")
                await self.bot.say("Désoler mais une partie est deja en cours !")

            elif djoueurs == 0:
                if gm == ctx.message.author:
                    djoueurs = 1
                    joueurs.insert(0, ctx.message.author.id)
                    print("Commande lg joueurs lancer par: "+str(ctx.message.author))
                    await self.bot.say("Rejoiner la partie avec la commande: ```lg join```.")

                else:
                    print("Commande lg joueurs lancer par: "+str(ctx.message.author)+", refuser car non GM")
                    await self.bot.say("Désoler mais vous n'étes pas le GM !")

    #Commande pour rejoindre la partie
    @lg.command(pass_context=True)
    async def join(self, ctx):
        global djoueurs,joueurs
        if game == 0:
            print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")

        elif game == 1:
            if djoueurs == 0:
                print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, definition des joueurs non lancer !")
                await self.bot.say("Désoler mais aucunne demande de joueurs est lancer !.")

            elif djoueurs == 2:
                print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, joueurs deja defini !")
                await self.bot.say("Désoler mais les joueurs sont deja defini.")

            elif djoueurs == 1:
                if gm == ctx.message.author:
                    print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, c'est le GM !")
                    await self.bot.say("Désoler mais vous êtes le GM, vous avez deja rejoint par defaut.")

                else:
                    joueurs.append(ctx.message.author.id)
                    print("Commande lg join lancer par: "+str(ctx.message.author))
                    await self.bot.say("Vous avez rejoin la partie !")

    #Commande pour stoper la definition de joueurs
    @lg.command(pass_context=True)
    async def play(self, ctx):
        global joueurs,gm,djoueurs,minijoueurs
        if game == 0:
            print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")

        elif game == 1:
            if djoueurs == 0:
                print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, definition des joueurs non lancer !")
                await self.bot.say("Désoler mais aucunne demande de joueurs est lancer !.")

            elif djoueurs == 2:
                print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, joueurs deja defini !")
                await self.bot.say("Désoler mais les joueurs sont deja defini.")

            elif djoueurs == 1:
                if gm == ctx.message.author:
                    if len(joueurs) < minijoueurs:
                        print("Commande lg play lancer par: "+str(ctx.message.author)+", refuser car minimum de joueurs pas atteint")
                        await self.bot.say("Désoler mais il n'y a que "+str(len(joueurs))+" joueur(s) dans la partie")

                    else:
                        djoueurs=2
                        print("Commande lg play lancer par: "+str(ctx.message.author))
                        await self.bot.say("Definitions de joueurs terminer !")
                        await self.bot.say("Il y a "+str(len(joueurs))+" joueurs dans la partie.")
                        await self.bot.say("Definitions du role de chacun des joueurs en cours...")


                else:
                    print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, pas le GM !")
                    await self.bot.say("Désoler mais vous n'êtes pas le GM !")

    #Commande de test
    @lg.command(pass_context=True)
    async def test(self, ctx):
        global gm,joueurs
        await self.bot.say("Liste de joueurs: "+str(joueurs))
        if gm == ctx.message.author:
	           await self.bot.say("vous etes le GM !")
        elif is_joueurs(ctx.message.author.id) == True:
            await self.bot.say("vous etes un joueurs !")


    #Commande pour annuler le Garou
    @lg.command(pass_context=True)
    async def stop(self, ctx):
        global game,djoueurs,gm
        if game == 0:
            print("Commande lg stop lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say("Désoler mais aucune partie n'est lancer.")

        elif game == 1:
            if gm == ctx.message.author:
                #reset de toutes les variables
                game = 0
                djoueurs = 0
                gm = str()
                joueurs = list()
                print("Commande lg stop lancer par: "+str(ctx.message.author))
                await self.bot.say("La partie de garou est annuler !")

            else:
                print("Commande lg stop lancer par: "+str(ctx.message.author)+" refuser car ce n'est pas le GM !")
                await self.bot.say("Désoler mais vous n'avez pas le droit de faire ça, vous n'étes pas le GM !")


def setup(bot):
    bot.add_cog(Garou(bot))
