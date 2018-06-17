import json
import discord
from discord.ext import commands

class Channeller:
    def __init__(self, bot):
        self.bot = bot
        with open('config.json') as json_data_file:
            parameter = json.load(json_data_file)

        self.owner = parameter['Perms']['Admin']

        self.server = self.bot.get_server("177396472294277120")
        self.ow_role = discord.utils.get(self.server.roles, name="🔫 Overwatch")

    ow_chan = dict()
    pv_chan = dict()

    """await def __unload(self):
        print("Channeller off")
        for c in self.ow_chan.values():
            await self.bot.delete_channel(c)"""

    def is_owner(self, id):
        if id in self.owner:
            return True
        return False

    #Groupe de commande du Channeller
    @commands.group(pass_context=True)
    async def channeller(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.help)

    #Le help
    @channeller.command(pass_context=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Channeller", description="Aide", color=0xff0000)
        embed.set_thumbnail(url="https://i.imgur.com/F7M1e6s.png")
        embed.add_field(name="jeux", value="Crée un channel vocal pour jouer !", inline=True)
        embed.add_field(name="private", value="Crée un channel vocal privée", inline=True)
        embed.add_field(name="publique", value="Crée un channel vocal publique", inline=True)
        await self.bot.say(embed=embed)

    #Crée un Channel jeux
    @channeller.command(pass_context=True)
    async def jeux(self, ctx, jeux):

        help=discord.Embed(title="Channeller jeux", description="Aide", color=0xff0000)
        help.set_thumbnail(url="https://i.imgur.com/F7M1e6s.png")
        help.add_field(name="overwatch", value="Crée un channel vocal pour jouer !", inline=True)
        help.add_field(name="fortinte", value="Crée un channel vocal privée", inline=True)  #TODO: Changer "fortninte",et mettre fortnite
        help.add_field(name="factorio", value="Crée un channel vocal publique", inline=True)
        help.add_field(name="minecraft", value="Crée un channel", inline=True)
        help.add_field(name="minecrafticka", value="Crée un channel vocal", inline=True)

        if jeux == "list":
            await self.bot.say(embed=help)

        elif jeux == None:
            await self.bot.say(embed=help)

        elif jeux == "overwatch":
            if self.ow_role in ctx.message.author.roles:
                everyone_perms = discord.PermissionOverwrite(connect=False)
                ow_perms = discord.PermissionOverwrite(connect=True)

                everyone = discord.ChannelPermissions(target=self.server.default_role, overwrite=everyone_perms)
                ow = discord.ChannelPermissions(target=self.ow_role, overwrite=ow_perms)

                name = "Overwatch "+str(len(self.ow_chan)+1)
                self.ow_chan[name] = await self.bot.create_channel(self.server, name, everyone, ow, type=discord.ChannelType.voice)
                embed=discord.Embed(title="Channeller jeux", description="Info", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/F7M1e6s.png")
                embed.add_field(name="jeux overwatch", value="Channel créé ! Déplacement automatique...", inline=True)
                await self.bot.say(embed=embed)
                print("Channel "+str(name)+" créé par: "+str(ctx.message.author))
                await self.bot.move_member(ctx.message.author, self.ow_chan[name])

            else:
                await self.bot.say("No")
                embed=discord.Embed(title="Channeller jeux", description="Erreur", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/F7M1e6s.png")
                embed.add_field(name="jeux overwatch", value="Désolé mais vous n'avez pas le grade du jeu corespondant !", inline=True)
                await self.bot.say(embed=embed)
                print("Refus de création d'un channel Overwatch, "+str(ctx.message.author)+" ne possède pas le grade")

        else:
            await self.bot.say(embed=help)

    @channeller.command(pass_context=True)
    async def private(self, ctx, nom, perso):

        if nom in self.pv_chan.values():
            print("nom deja existant !")

        else:
            everyone_perms = discord.PermissionOverwrite(connect=False)
            pv_perms = discord.PermissionOverwrite(connect=True)

            everyone = discord.ChannelPermissions(target=self.server.default_role, overwrite=everyone_perms)
            pv = discord.ChannelPermissions(target=ctx.message.author, overwrite=pv_perms)

            self.pv_chan[nom] = await self.bot.create_channel(self.server, nom, everyone, pv, type=discord.ChannelType.voice)

            """for player in perso:
                test"""
            print(perso)

            embed=discord.Embed(title="Channeller priver", description="Info", color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/F7M1e6s.png")
            embed.add_field(name="Priver", value="Channel créé ! Déplacement automatique...", inline=True)
            await self.bot.say(embed=embed)
            print("Channel "+str(nom)+" créé par: "+str(ctx.message.author))
            await self.bot.move_member(ctx.message.author, self.pv_chan[nom])

    """@channeller.command(pass_contexte=True)
    async def delete(self):
        for n in range(0, self.ow_num):
            await self.bot.delete_channel(self.ow_chan["ow_"+str(n+1)])
        self.ow_chan = dict()"""

    async def on_voice_state_update(self, x, y):
        #OW clear
        for c in self.ow_chan.values():
            self.ow_chan[str(c)] = self.bot.get_channel(c.id)
            if len(self.ow_chan[str(c)].voice_members) == 0:
                await self.bot.delete_channel(c)
                del self.ow_chan[str(c)]

        #PV clear
        for c in self.pv_chan.values():
            self.pv_chan[str(c)] = self.bot.get_channel(c.id)
            if len(self.pv_chan[str(c)].voice_members) == 0:
                await self.bot.delete_channel(c)
                del self.pv_chan[str(c)]


def setup(bot):
    bot.add_cog(Channeller(bot))
    print("Channeller chargé")
