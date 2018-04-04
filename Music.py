import asyncio
import discord
from discord.ext import commands
from ctypes.util import find_library
import youtube_dl
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus(find_library("opus"))

def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            print("Musique en cours lancée: "+str(self.current))
            #await self.bot.change_presence(game=discord.Game(name='faire de la musique: '+str(self.current)))
            embed=discord.Embed(title="Musique", description="En cours", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="play", value="Jouée acutellement: \n" + str(self.current), inline=True)
            await self.bot.send_message(self.current.channel, embed=embed)
            self.current.player.start()
            await self.play_next_song.wait()
        

class Musique:
    """Commandes de musique.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    def set_pause(self, server):
            state = self.get_voice_state(server)
            player = state.player
            player.pause()

    def set_resume(self,server):
        state = self.get_voice_state(server)
        player = state.player
        player.resume()

    def is_listening(self, user_channel):
        for bot_channel in self.bot.voice_clients:
            if bot_channel.channel == user_channel:
                return True
            return False

    #Definition du group music
    @commands.group(pass_context=True)
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.help)

    #Un simple help
    @music.command(pass_context=True, no_pm=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Musique", description="Aide", color=0x80ff00)
        embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
        embed.add_field(name="play", value="Lancer une musique", inline=True)
        embed.add_field(name="playing", value="Voir quelle musique est lancée", inline=True)
        embed.add_field(name="pause", value="Met en pause la musique", inline=True)
        embed.add_field(name="resume", value="Résume la musique", inline=True)
        embed.add_field(name="skip", value="Passer la musique", inline=True)
        embed.add_field(name="stop", value="Arrêter la musique", inline=True)
        embed.add_field(name="summon", value="Faire apparaître le bot", inline=True)
        embed.add_field(name="volume", value="Définir le volume de la musique", inline=True)
        await self.bot.say(embed=embed)

    #Permmet de faire connecter vocalement le bot
    @music.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Invoque le bot dans le channel vocal.
        Ne fonctionne que si l'utilisateur est déja dans un channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            print("Commande musique summon lancée par: "+str(ctx.message.author)+" refuser car il n'est pas dans un channel vocal")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="summon", value="Vous n'êtes pas dans un channel vocal !", inline=True)
            await self.bot.say(embed=embed)
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            print("Commande musique summon lancée par: "+str(ctx.message.author))
            state.voice = await self.bot.join_voice_channel(summoned_channel)
            embed=discord.Embed(title="Musique", description="", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="summon", value="Il se matérialise devant vous !", inline=True)
            await self.bot.say(embed=embed)
        else:
            print("Commande music summon lancée par: "+str(ctx.message.author))
            await state.voice.move_to(summoned_channel)
            embed=discord.Embed(title="Musique", description="", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="summon", value="Il se téléporte a vous !", inline=True)
            await self.bot.say(embed=embed)

        return True

    #Permet de mettre a jouer une musique
    @music.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Joue une musique.
        S'il y a une musique qui joue déjà, alors elle est mise dans
        la queue jusqu'a la derniere musique de la queue.
        Le bot recherche automatiquement sur youtube.
        La liste des sites supportés est trouvée ici:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            "format":"bestaudio/worstvideo",
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            print("Commande musique play lancée par: "+str(ctx.message.author))
            #embed=discord.Embed(title="Musique", description="", color=0x80ff00)
            #embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            #embed.add_field(name="play", value="Chargement de la musique...", inline=True)
            message = await self.bot.say("Chargement de la musique...")
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
            #await self.bot.delete_message(message)


        except Exception as e:
            fmt = 'Une erreur est arrivé lors du traitement de la requete: ```py\n{}: {}\n```'
            print("Commande musique play lancée par: "+str(ctx.message.author)+" erreur: "+fmt.format(type(e).__name__, e))
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="play", value=fmt.format(type(e).__name__, e), inline=True)
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            print("Commande musique play lancée par: "+str(ctx.message.author)+" mise en queue")
            embed=discord.Embed(title="Musique", description="", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="play", value="La musique \n" + str(entry)+" \na été mise en queue", inline=True)
            await self.bot.say(embed=embed)
            await state.songs.put(entry)

    #Permmet de definit le volume
    @music.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Définie le volume du bot."""
        voice_channel_id = ctx.message.author.voice_channel
        if self.is_listening(voice_channel_id) == True:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                player.volume = value / 100
                print("Commande music volume lancée par: "+str(ctx.message.author))
                embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="volume", value='Volume mit à {:.0%}'.format(player.volume), inline=True)
                await self.bot.say(embed=embed)

        elif self.is_listening(voice_channel_id) == False:
            print("Commande music volume lancée par: "+str(ctx.message.author)+" refuser car il n'est pas dans le channel vocal")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="volume", value="Vous n'étes pas dans le channel vocal !", inline=True)
            await self.bot.say(embed=embed)

    #MEt en pause la musique
    @music.command(pass_context=True,no_pm=True)
    async def pause(self,ctx):
        voice_channel_id = ctx.message.author.voice_channel
        if self.is_listening(voice_channel_id) == True:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                print("Commande musique pause lancée par: "+str(ctx.message.author))
                embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="pause", value="Mise en pause de la musique", inline=True)
                await self.bot.say(embed=embed)
                await self.set_pause(ctx.message.author.server)

        elif self.is_listening(voice_channel_id) == False:
            print("Commande musique resume lancée par: "+str(ctx.message.author)+" refuser car il n'est pas dans le channel vocal")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="resume", value="Vous n'étes pas dans le channel vocal !", inline=True)
            await self.bot.say(embed=embed)


    #Reprend la music
    @music.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        voice_channel_id = ctx.message.author.voice_channel
        if self.is_listening(voice_channel_id) == True:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                print("Commande musique resume lancée par: "+str(ctx.message.author))
                embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="resume", value="Reprise de la musique", inline=True)
                await self.bot.say(embed=embed)
                await self.set_resume(ctx.message.author.server)

        elif self.is_listening(voice_channel_id) == False:
            print("Commande musique resume lancée par: "+str(ctx.message.author)+" refuser car il n'est pas dans le channel vocal")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="resume", value="Vous n'étes pas dans le channel vocal !", inline=True)
            await self.bot.say(embed=embed)

    async def on_voice_state_update(self,before,after):
        state = self.get_voice_state(after.server)
        if type(state.voice) != type(None):
            if type(before.voice_channel) != type(None):
                if state.voice.channel == before.voice_channel:
                    if len(before.voice_channel.voice_members)<2:
                        try:await self.get_pause(state.voice.channel.server)
                        except:pass
            if type(after.voice_channel) != type(None):
                if len(after.voice_channel.voice_members)>=2:
                    try:await self.get_resume(state.voice.channel.server)
                    except:pass

    #Arret la musique et fait quitter le bot
    @music.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Arrete la musique jouée et quitte le channel.
        Cela vide aussi la queue.
        """
        voice_channel_id = ctx.message.author.voice_channel
        if self.is_listening(voice_channel_id) == True:
            server = ctx.message.server
            state = self.get_voice_state(server)

            if state.is_playing():
                player = state.player
                player.stop()

            try:
                state.audio_player.cancel()
                del self.voice_states[server.id]
                await state.voice.disconnect()
                print("Commande musique stop lancée par: "+str(ctx.message.author))
                embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="stop", value="Queue vidée et channel quitté.", inline=True)
                await self.bot.say(embed=embed)
            except:
                pass

        elif self.is_listening(voice_channel_id) == False:
            print("Commande musique stop lancée par: "+str(ctx.message.author)+" refuser car il n'est pas dans le channel vocal")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="stop", value="Vous n'étes pas dans le channel vocal !", inline=True)
            await self.bot.say(embed=embed)

    #Permet de passer la musique en cours
    @music.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote pour passer la chanson en cours.
        Il faut trois votes pour passer la chanson.
        """
        voice_channel_id = ctx.message.author.voice_channel
        if self.is_listening(voice_channel_id) == True:
            state = self.get_voice_state(ctx.message.server)
            if not state.is_playing():
                print("Commande musique skip lancée par: "+str(ctx.message.author)+" refuser car rien est jouer")
                embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="skip", value="Aucune chanson n'est jouée actuellement...", inline=True)
                await self.bot.say(embed=embed)
                return

            voter = ctx.message.author
            if voter == state.current.requester:
                print("Commande musique skip lancée par: "+str(ctx.message.author)+" requete envoyer")
                embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="skip", value="Une requete pour passer la chanson a été faite.", inline=True)
                await self.bot.say(embed=embed)
                state.skip()
            elif voter.id not in state.skip_votes:
                state.skip_votes.add(voter.id)
                total_votes = len(state.skip_votes)
                if total_votes >= 3:
                    print("Commande musique skip lancée")
                    embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                    embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                    embed.add_field(name="skip", value="Vote pour passer effectué, chanson passée...", inline=True)
                    await self.bot.say(embed=embed)
                    state.skip()
                else:
                    embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                    embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                    embed.add_field(name="skip", value="Vote pour passer effectué, actuellement à [{}/3]".format(total_votes), inline=True)
                    await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Musique", description="", color=0x80ff00)
                embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
                embed.add_field(name="skip", value="Vous avez déjà voté pour passer cette chanson.", inline=True)
                await self.bot.say(embed=embed)

        elif self.is_listening(voice_channel_id) == False:
            print("Commande musique skip lancée par: "+str(ctx.message.author)+" refuser car il n'est pas dans le channel vocal")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="skip", value="Vous n'étes pas dans le channel vocal !", inline=True)
            await self.bot.say(embed=embed)

    #Affiche la musique actuellement lancée
    @music.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            print("Commande musique playing lancée par: "+str(ctx.message.author)+" refuser car rien est jouer")
            embed=discord.Embed(title="Musique", description="Erreur", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="playing", value="Aucune chanson n'est jouée actuellement...", inline=True)
            await self.bot.say(embed=embed)
        else:
            skip_count = len(state.skip_votes)
            print("Commande musique playing lancée par: "+str(ctx.message.author))
            embed=discord.Embed(title="Musique", description="", color=0x80ff00)
            embed.set_thumbnail(url="http://www.icone-png.com/png/16/15638.png")
            embed.add_field(name="playing", value="Jouée actuellement {} [skips: {}/3]".format(state.current, skip_count), inline=True)
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Musique(bot))
    print('Musique chargée')
