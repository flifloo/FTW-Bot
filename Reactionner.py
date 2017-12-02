import discord
from discord.ext import commands

licorne_symbole = "🦄"
licorne = ["licorne"]

caca_symbole = "💩"
caca = ["caca", "merde"]

sel_symbole = ":PJSalt:232086190545829888"
sel = ["sel", "salty", "putain"]

troll_symbole = ":troll:232080409083641856"
troll = ["troll", "trol", "trololo"]

class Reactionner:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        for i in range(len(licorne)):
            if licorne[i] in message.content.lower():
                print("licorne detecter !")
                await self.bot.add_reaction(message,licorne_symbole)
        
        for i in range(len(caca)):
            if caca[i] in message.content.lower():
                print("caca detecter !")
                await self.bot.add_reaction(message,caca_symbole )
                
        for i in range(len(sel)):
            if sel[i] in message.content.lower():
                print("sel detecter !")
                await self.bot.add_reaction(message,sel_symbole)
                
        for i in range(len(troll)):
            if troll[i] in message.content.lower():
                print("troll detecter !")
                await self.bot.add_reaction(message,troll_symbole)

def setup(bot):
    bot.add_cog(Reactionner(bot))