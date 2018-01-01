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
            await self.bot.send_message(self.current.channel, ' Joue maintenant ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
class Music:
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

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Rejoins le channel vocal. Ne fonctionne que si l'utilisateur est deja dans un channel.
        Ne semble pas fonctionner pour le moment."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in **' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Invoque le bot dans le channel vocal.
        Ne fonctionne que si l'utilisateur est déja dans un channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('Are you sure your in a channel?')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Joue une musique.
        S'il y a une musique qui joue deja, alors elle est mise dans
        la queue jusqu'a la derniere musique de la queue.
        Le bot recherche automatiquement sur youtube.
        La liste des sites supportés est trouvée ici:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            await self.bot.say("Chargement de la musique...")
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'Une erreur est arrivé lors du traitement de la requete: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('La musique ' + str(entry)+" a été mise en queue")
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Définie le volume du bot."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Volume mit à {:.0%}'.format(player.volume))
    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Relance la misique jouée."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Arrete la musique jouée et quitte le channel.
        Cela vide aussi la queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("Queue vidée et channel quitté. ")
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote pour passer la chanson en cours.
        Il faut trois votes pour passer la chanson.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say("Aucune chanson n'est jouée actuellement...")
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Une requete pour passer la chanson a été faite.')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Vote pour passer effectué,chanson passée...')
                state.skip()
            else:
                await self.bot.say('Vote pour passer effectué, actuellement à [{}/3]'.format(total_votes))
        else:
            await self.bot.say('Vous avez deja voté pour passer cette chanson.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Montre des informations sur la chanson jouée."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say("Rien n'est joué.")
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Joue actuellement {} [skips: {}/3]'.format(state.current, skip_count))
            
def setup(bot):
    bot.add_cog(Music(bot))
    print('Music is loaded')
