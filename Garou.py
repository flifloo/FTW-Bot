import discord
import random
from discord.ext import commands

game = 0
djoueurs = 0
joueurs = str("0")



class Garou:
    def __init__(self, bot):
        self.bot = bot
        self.games = {} # contiendra toutes les partie en cours


    def create_game(self, channel_id): # créer une game : ajout d'option possible
        game = {
            'channel' : channel_id,
            'player' : [],
            'message' : None
        }
        return game

    def get_game(self,channel_id):
        for game in self.games:
            if channel_id == game['channel']:
                return game
        return None


    def embed(self):
        info = discord.Embed()
        info.title = 'Garou : Choose the player'
        info.colour = random.randint(0, 0xFFFFFF)
        info.add_field(name='Description', value="Voici une description ndu jeu")
        info.add_field(name='Info', value="Choose the player by react on this message !")
        info.set_footer(text="Loup Garou by jbdo99 & flifloo")
        return info



    #Commande de démarrage du Garou
    @commands.command(pass_context=True, name="lg")
    async def start(self, ctx):
        """Commence la partie"""
        if self.get_game(ctx.message.channel) == None: # on verifie si il n y pas de partie en cours dans ce salon
            self.games[ctx.message.channel] = self.create_game(ctx.message.channel) # on créer le jeu
            game = self.games[ctx.message.channel]
            game['message'] = await self.bot.send_message(ctx.message.channel,embed=self.embed()) # on affiche le message et on le met dans le game
            for emoji in ["💚"]:
                await self.bot.add_reaction(message=game["message"],emoji=emoji) #on fai apparaitre le/les reac du bot
            nopi = True
            while nopi:
                waiter = await self.bot.wait_for_reaction(message=game["message"],timeout=40.0)
                if not waiter == None:
                    if (waiter[0].emoji == "💚"):
                        await self.bot.say("Un joueur en plus !")
        else:
            await self.bot.say("A game already started")
"""
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
                await self.bot.say("Désoler mais une partie est deja en cours !")

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
"""

def setup(bot):
    bot.add_cog(Garou(bot))
