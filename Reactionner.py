import discord
from discord.ext import commands

licorne_symbole = "🦄"
licorne = ["licorne", "pony", "poney"]

caca_symbole = "💩"
caca = ["caca", "merde", "crotte", "bouse"]

sel_symbole = ":PJSalt:232086190545829888"
sel = ["sel", "salty", "putain"]

troll_symbole = ":troll:232080409083641856"
troll = ["troll", "trol", "trololo"]

dog_symbole = "🐶"
dog = ["waf", "ouaf", "chien", "dog", "wouaf"]

perfect_symbole = "👌"
perfect = ["parfait", "perfect", "ok"]

plus_symbole = ":plus:283940426053058561"
plus = ["+1"]

class Reactionner:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        for i in range(len(licorne)):
            if licorne[i] in message.content.lower():
                print("Licorne detectée !")
                await self.bot.add_reaction(message,licorne_symbole)

        for i in range(len(caca)):
            if caca[i] in message.content.lower():
                print("Caca detecté !")
                await self.bot.add_reaction(message,caca_symbole )

        for i in range(len(sel)):
            if sel[i] in message.content.lower():
                print("Sel detecté !")
                await self.bot.add_reaction(message,sel_symbole)

        for i in range(len(troll)):
            if troll[i] in message.content.lower():
                print("Troll detecté !")
                await self.bot.add_reaction(message,troll_symbole)

        for i in range(len(dog)):
            if dog[i] in message.content.lower():
                print("Chien detecté !")
                await self.bot.add_reaction(message,dog_symbole)

        for i in range(len(perfect)):
            if perfect[i] in message.content.lower():
                print("Perfection detecté !")
                await self.bot.add_reaction(message,perfect_symbole)

        for i in range(len(plus)):
            if plus[i] in message.content.lower():
                print("Plus detecté !")
                await self.bot.add_reaction(message,plus_symbole)

def setup(bot):
    bot.add_cog(Reactionner(bot))
    print("Reactions chargé")
