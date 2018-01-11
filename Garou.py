import discord
import random
from random import randint
from discord.ext import commands


class Garou:
    def __init__(self, bot):
        self.bot = bot
        self.discord = discord

    #Variables de base
    game = 0 #Dit si une partie est en cours
    djoueurs = 0 #Dit si les joueurs sont defini ou entrain d'étres defini ou non
    gm = () #Dit qui est le GM (ID)
    list_joueurs = [] #Dit qui sont les joueurs (ID)
    ult_list_joueurs = [] #Dit qui sont les joueurs (Object)
    def_joueurs = dict() #Dit qui sont les joeurs defini avec leur roles
    random = [0] #Liste des chiffre random tiré
    num_joueurs = 0 #Nombre de joueurs dans la partie

    #Vrai variables
    minijoueurs = 1 #5, Le nombre minimum de joueurs qu'il faut pour lancer une partie
    roles = ["0", "LG", "VY", "VO", "SO", "VG", "VG", "CS", "CU", "LG", "CL", "AG", "MA", "IL", "IPDL", "JDF", "VG", "RE", "GML", "VG", "LGB", "VG", "SA", "LG", "AS", "CER", "MO", "AC", "SE", "SE", "IDV", "BE", "ES", "KZ", "ISM", "VG"] #Les roles donner

    #text time
    def intro(self, role):
        if role == "VG":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Villageois")
            intro.add_field(name="Votre personnage : ", value="*A Thiercelieu les habitants sont victimes d’une terrible malédiction, chaque jour ils tentent de tuer un loup-garou en votant*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous, à chaque journée, vous votez avec le reste des joueurs pour tenter d’éliminer les loups-garous.**", inline=False)
            return intro

        elif role == "LG":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Loup-garou")
            intro.add_field(name="Votre personnage : ", value="*Le village de Thiercelieu est victime d’une terrible malédiction. Des loups-garous terrorisent les habitants de cette petite bourgade et dévorent les villageois.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les villageois. Chaque nuit, vous décidez, avec les autres loups-garous, de tuer une personne.**", inline=False)
            return intro

        elif role =="VY":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Voyante")
            intro.add_field(name="Votre personnage : ", value="*Cette personne si secrète pourra-t-elle faire la lumière sur les évènements de Thiercelieu ? Ces dons bizarres pour la voyance lui permettent de connaitre la véritable nature des gens.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous pourrez connaitre le rôle d’une personne.**", inline=False)
            return intro

        elif role == "VO":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Voleur")
            intro.add_field(name="Votre personnage : ", value="*Qui est donc ce chapardeur qui met la confusion dans la tête des gens ? Il n’est pas méchant, mais des gens disent qu’il manipulerait les autres.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Toutes les deux nuits, vous échangerez les rôles de deux personnes. **", inline=False)
            return intro

        elif role =="SO":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Sorcière")
            intro.add_field(name="Votre personnage : ", value="*Quelle est cette femme qui concocte ses potions en secret, décidant du sort de ses victimes ? On la dit capable de soigner, mais aussi de tuer.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous pouvez soigner ou tuer une personne, ou ne rien faire. Attention, chaque potion ne peut être utilisé qu’une seule fois.**", inline=False)
            return intro

        elif role == "CS":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Chasseur")
            intro.add_field(name="Votre personnage : ", value="*Cet homme seul à décider de prendre les armes et de traquer les loups-garous qui terrorisent le village. Qui sait ce que pourrait faire un homme armé au bord de la mort ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Si vous êtes tué, vous pourrez tuer une autre personne avant de mourir.**", inline=False)
            return intro

        elif role == "CU":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Cupidon")
            intro.add_field(name="Votre personnage : ", value="*Qui recevra les flèches de l’amour lancées par ce petit être ? Ceux-ci se voueront un amour pur et total, et dépendrons l’un de l’autre.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. En début de partie, vous rendrez deux personnes amoureuses. Celles-ci seront dépendante l’une de l’autre, et si l’une meurt, l’autre se tuera de chagrin.**", inline=False)
            return intro

        elif role == "CL":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Chien-loup")
            intro.add_field(name="Votre personnage : ", value="*Il existe à Thiercelieu une espèce de chien très rares, pouvant adopter des comportements violents. Deviendra-t-il loup-garou, ou restera t-il un chien docile ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**En début de partie vous aurez le choix entre rejoindre les loups-garous ou les villageois.**", inline=False)
            return intro

        elif role == "AG":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Ange")
            intro.add_field(name="Votre personnage : ", value="*Ce petit homme volant ce fiche éperdument du sort d’un petit village perdu au fond des landes. Tout ce qu’il veut c’est s’envoler un retrouver le calme des cieux.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de gagner la partie seul. Si vous êtes tué par les villageois au premier jour, vous remportez la partie. Sinon, vous devenez simple villageois.**", inline=False)
            return intro

        elif role == "MA":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Maire")
            intro.add_field(name="Votre personnage : ", value="*Tout village, même dans la terreur, a besoin d’un leader en qui avoir confiance.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Votre vote compte double.**", inline=False)
            return intro

        elif role == "IL":
            ntro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Illettré")
            intro.add_field(name="Votre personnage : ", value="*L’éducation est privilège dont tout le monde devrait avoir accès. Cette personne étrangère ne comprend rien aux paroles des autres habitants. De temps en temps il aime se balader la nuit, il voit des choses étranges, sans savoir ce qu’elles sont.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Chaque nuit, vous percevez des morceaux de la conversation des loups-garous.**", inline=False)
            return intro

        elif role == "IPDL":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Infect père des loups")
            intro.add_field(name="Votre personnage : ", value="*Même les loups-garous ont une famille. Cette famille-là est ancienne est terrible, capable de pervertir le cœur des plus nobles.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les villageois. Une fois par partie, vous pouvez infecter une personne désignée comme victime par les loups-garous. Celle-ci ne sera pas tuée mais deviendra secrètement un loup-garou.**", inline=False)
            return intro

        elif role == "JDF":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Joueur de flûte")
            intro.add_field(name="Votre personnage : ", value="*Cet homme, autrefois banni, et aujourd’hui oublié, revient au village pour se venger. Armé de sa flûte à bec, il prend peu à peu possession du village à qui il souhaite donner une leçon.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de contaminer tous les habitants du village. Chaque nuit, vous contaminez une ou deux personnes.**", inline=False)
            return intro

        elif role == "RE":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Renard")
            intro.add_field(name="Votre personnage : ", value="*Les loups ne sont pas les seuls animaux à Thiercelieu. Ce renard rusé serait capable de sentir l’âme des gens ainsi que leurs intentions.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous voyez le rôle de trois personnes, mais si aucune d’elles n’est un loup-garou, vous perdez votre pouvoir.**", inline=False)
            return intro

        elif role == "GML":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Grand méchant loup")
            intro.add_field(name="Votre personnage : ", value="*Il n’y a pas que les trois petits cochons qui craignent le grand méchant loup. Celui est encore plus meurtrier est assoiffé de sang que ses semblables.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les villageois. Tant qu’aucun loup-garou n’est mort, vous pouvez tuer une personne supplémentaire par nuit.**", inline=False)
            return intro

        elif role == "LGB":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Loup-garou blanc")
            intro.add_field(name="Votre personnage : ", value="*Il y aurait un traitre dans les rangs des loups-garous. Celui-ci les éliminerait de l’intérieur, un à un.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de finir la partie seul. Toutes les deux nuits, vous pouvez tuer un loup-garou, en plus de la victime de chaque nuit.**", inline=False)
            return intro

        elif role == "SA":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Salvateur")
            intro.add_field(name="Votre personnage : ", value="*A Thiercelieu, ce personnage est devenu une légende. Sa bénédiction permettrait de se protéger des événements récents.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous accordez votre bénédiction à une personne. Celle-ci ne pourra pas être tuée pendant la nuit.**", inline=False)
            return intro

        elif role == "AS":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Assassin")
            intro.add_field(name="Votre personnage : ", value="*A Thiercelieu, il y a un fou qui n’avait jusque-là jamais été dangereux. Mais les récents évènements ont perturbé sa santé mentale. Depuis, il vit dans une folie meurtrière qui ne peut contrôler.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de finir la partie seul. Chaque matin, vous tuez une personne au hasard.**", inline=False)
            return intro

        elif role == "CER":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Chevalier à l’épée rouillée")
            intro.add_field(name="Votre personnage : ", value="*Don Quigrince était un fier chevalier vaillant ayant participé à de nombreuses batailles. Aujourd’hui, le temps et le manque d’action se sont transformés en ennui. Il ne mange plus, dors peu, et ne s’est pas occupé de son épée depuis fort longtemps. Celle-ci s’est émoussée, et pourrait surement empoissonner un loup trop gourmand.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Si vous êtes tué par les loup-garou, celui qui avait proposé votre mort sera tué la nuit suivante.**", inline=False)
            return intro

        elif role == "MO":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Montreur d’ours")
            intro.add_field(name="Votre personnage : ", value="*En plus des loups-garous, il y a un ours qui rode dans les bois de Thiercelieu. Celui-ci est très grincheux, et n’hésitera pas à grogner pour effrayer les loups-garous trop curieux.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, si un loup-garou se trouve à coté de vous, vous grognez.**", inline=False)
            return intro

        elif role == "AC":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Ancien")
            intro.add_field(name="Votre personnage : ", value="*L’expérience amène la sagesse. Et la sagesse amène la maitrise de soi. Le doyen du village l’a bien compris. Bien qu’étant d’un âge avancé, il saura s’enfuir face aux loups-garous qui essayeraient de le tuer. Cependant, sa mort démoraliserait tous les villageois.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer les loups-garous. Si vous êtes tué par les loups garous, vous pourrez échanger votre rôle avec une personne au hasard la nuit suivante. Si vous êtes tué une deuxième fois, tous les villageois restants perdrons leurs pouvoirs.**", inline=False)
            return intro

        elif role == "SE":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Sœur")
            intro.add_field(name="Votre personnage : ", value="*Rien n’est plus beau que la fraternité. Ces deux sœurs sont comme deux doigts d’une même main, ou deux cheveux d’une même mèche. Elles se comprennent sans même se parler.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les villageois. Certaines nuits, vous serez appelés, et pourrait communiquer avec l’autre sœur.**", inline=False)
            return intro

        elif role == "IDV":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Idiot du village")
            intro.add_field(name="Votre personnage : ", value="*Les villageois ont beau essayer d’en faire quelque chose, il ne comprend rien de rien. Cependant, ils ne pourront jamais lui faire de mal. Même au moment de le tuer, ils décideront de ne rien lui faire, et de ne plus lui parler. Qui écouterait un idiot ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Si vous êtes tué par les villageois, vous serez acquitté mais perdrez votre droit de vote.**", inline=False)
            return intro

        elif role == "ES":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Enfant sauvage")
            intro.add_field(name="Votre personnage : ", value="*Cet enfant est sorti de la forêt un jour, sans prévenir. Il a été élevé par les loups, dans les bois. Cependant, il essaye de s’intégrer dans le village, en prenant un modèle. Qui sait ce qu’il pourrait devenir s’il lui arrivait quelque chose ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**En début de partie, vous choisissez un modèle. Tant que cette personne est en vie, vous restez villageois, mais si elle meurt, vous vous transformez en loup-garou.**", inline=False)
            return intro

        elif role == "BE":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Bouc-émissaire")
            intro.add_field(name="Votre personnage : ", value="*Qu’est-ce que cet homme a bien pu faire pour être autant détester par le village ? En cas de doute, c’est toujours de sa faute.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Si les villageois doutent sur qui tuer pendant le vote, vous serez tué par défaut.**", inline=False)
            return intro

        elif role == "KZ":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Kamikaze")
            intro.add_field(name="Votre personnage : ", value="*Cet homme au passif si tumultueux n’a plus rien à perdre. Il serait prêt à risquer sa vie pour faire entendre raison aux autres villageois.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups garous. Une fois par partie, vous pouvez à tout moment tuer une autre personne, mais vous mourrez en faisant cela.**", inline=False)
            return intro

        elif role == "ISM":
            intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            intro.add_field(name="Vous êtes : ", value="Insomniaque")
            intro.add_field(name="Votre personnage : ", value="*Les problèmes de sommeil sont terribles. Mais cela permet de savoir tout avant les autres. Impossible de savoir ce qui empêche cette femme de dormir. Peut-être ce qu’elle apprend le matin, à l’aube.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups –garous. Toutes les nuits, vous saurez le dérouler exact de tout la nuit.**", inline=False)
            return intro

    #Erreur de partie deja en cours
    erreur1=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
    erreur1.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
    erreur1.add_field(name="Imposible", value="Désoler mais une partie est deja en cours !", inline=False)

    #Erreur de partie non lancer
    erreur2=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
    erreur2.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
    erreur2.add_field(name="Imposible", value="Désoler mais aucune partie en cours !", inline=False)

    #Erreur de ne pas étre le GM
    erreur3=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
    erreur3.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
    erreur3.add_field(name="Imposible", value="Désoler mais vous n'étes pas le GM !", inline=False)


    #Pour verifier que la personne donner soit bien un joueur
    def is_joueurs(self, target):
        for j in self.def_joueurs:
            if target in j:
                return True
        return False

    #Définition du groupe de commande lg
    @commands.group(pass_context=True)
    async def lg(self, ctx):
        if ctx.invoked_subcommand is None:
            #Affiche le help au cas ou de commande vide ou incorrecte
            await ctx.invoke(self.help)


    #Commande pour démarre le jeux
    @lg.command(pass_context=True)
    async def start(self, ctx):
        if self.game == 1: #Verification si une partie est deja lancer
            print("Commande lg start lancer par: "+str(ctx.message.author)+" refuser, partie deja lancer")
            await self.bot.say(embed=self.erreur1)

        else:
            if self.djoueurs >= 1: #Verification si les joueurs sont deja defini
                print("Commande lg start lancer par: "+str(ctx.message.author)+" refuser, partie deja lancer")
                await self.bot.say(embed=self.erreur1)

            else:
                print("Commande lg start lancer par: "+str(ctx.message.author))
                self.game=1 #On dit qu'une la partie est lancer
                self.gm=ctx.message.author #On defini le GM
                self.djoueurs = 1 #On dit qu'on defini les joueurs
                self.list_joueurs.insert(0, ctx.message.author.id) #On ajoute le GM dans la liste de joueurs (ID)
                self.ult_list_joueurs.insert(0,ctx.message.author) #On ajoute le GM dans la liste de joueurs (Object)
                embed=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                embed.add_field(name="Début de partie", value="Une partie a été lancer par: "+str(ctx.message.author)+" ! \nPour rejoindre, taper la commande: ```lg join```", inline=False)
                await self.bot.say(embed=embed)


    #Commande pour rejoindre la partie
    @lg.command(pass_context=True)
    async def join(self, ctx):
        if self.game == 0: #Verification si une partie est deja lancer
            print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        else:
            if self.djoueurs == 2: #Verification si les joueurs sont deja defini
                print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, joueurs deja defini !")
                await self.bot.say(embed=self.erreur1)

            elif self.djoueurs == 1: #Verification si les joueurs sont en cours de definition
                if self.gm == ctx.message.author: #Verification si c'est le GM
                    print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, c'est le GM !")
                    embed=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
                    embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    embed.add_field(name="Imposible", value="Désoler mais vous êtes le GM, vous avez deja rejoint par defaut.", inline=False)
                    await self.bot.say(embed=embed)

                else:
                    print("Commande lg join lancer par: "+str(ctx.message.author))
                    self.list_joueurs.append(ctx.message.author.id)
                    self.ult_list_joueurs.append(ctx.message.author)
                    embed=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
                    embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    embed.add_field(name="Début de partie", value=str(ctx.message.author)+" a rejoint !", inline=False)
                    await self.bot.say(embed=embed)


    #Commande pour lancer la partie
    @lg.command(pass_context=True)
    async def play(self, ctx):
        if self.game == 0: #Verification si une partie est deja lancer
            print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        else:
            if self.djoueurs == 0: #Verification si les joueurs sont deja defini
                print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, definition des joueurs non lancer !")
                await self.bot.say(embed=self.erreur2)

            elif self.djoueurs == 2: #Verification si les joueurs sont deja defini
                print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, joueurs deja defini !")
                await self.bot.say(embed=self.erreur1)

            elif self.djoueurs == 1: #Verification si les joueurs sont en cours de definition
                if self.gm == ctx.message.author: #Verification si c'est le GM
                    if len(self.list_joueurs) < self.minijoueurs: #Verification du nombre de joueurs minimal requi
                        print("Commande lg play lancer par: "+str(ctx.message.author)+", refuser car minimum de joueurs pas atteint")
                        embed=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
                        embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                        embed.add_field(name="Imposible", value="Désoler mais il n'y a que "+str(len(self.list_joueurs))+" joueur(s) dans la partie", inline=False)
                        await self.bot.say(embed=embed)

                    else:
                        self.djoueurs=2 #On dit que les joueurs sont defini
                        self.num_joueurs=len(self.list_joueurs) #On defini combien de joueurs en tout
                        print("Commande lg play lancer par: "+str(ctx.message.author))

                        #Definition des roles
                        for j in range(0,self.num_joueurs): #Un boucle qui fait autent de fois qu'il y a de joueurs
                            target = self.list_joueurs[j] #Prend dans la liste des joueurs le joueur en question.
                            while self.is_joueurs(target) != True: #Boucle tant que le jouer n'est pas dans la liste des personnes défini
                                r = randint(1,self.num_joueurs) #Tire un chiffre random entre 1 et le nombre de jouers
                                if r not in self.random: #Si se chiffre a deja éter tiré, alors sela relance le while
                                    self.def_joueurs[target] = self.roles[r] #Ajoute dans le dico le joueur et assigne son role grace au chiffre random
                                    self.random.append(r) #Ajoute le chiffre random dans la liste des chiffres deja tiré

                                    #Envoie du message de role
                                    client = self.ult_list_joueurs[j] #Cible le joueur en question mais cette fois son objet et non son ID
                                    embed = self.intro(self.roles[r])
                                    await self.bot.send_message(client, embed=embed)


                                    print(self.def_joueurs) #On log les roles

                        embed=discord.Embed(title="Garou", description="Démarrage", color=0xff0000)
                        embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                        embed.add_field(name="Début de partie", value="Definitions de joueurs terminer ! \nIl y a "+str(self.num_joueurs)+" joueurs dans la partie. \nDefinitions du role de chacun des joueurs en cours, ils vous seront envoyer par MP !", inline=False)
                        await self.bot.say(embed=embed)


                else:
                    print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, pas le GM !")
                    await self.bot.say(embed=self.erreur3)

    #Commande pour annuler le Garou
    @lg.command(pass_context=True)
    async def stop(self, ctx):
        if self.game == 0:
            print("Commande lg stop lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        elif self.game == 1:
            if self.gm == ctx.message.author:
                print("Commande lg stop lancer par: "+str(ctx.message.author))

                #reset de toutes les variables
                game = 0
                djoueurs = 0
                gm = ()
                list_joueurs = []
                ult_list_joueurs = []
                def_joueurs = dict()
                random = [0]
                num_joueurs = 0
                
                embed=discord.Embed(title="Garou", description="Attention", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                embed.add_field(name="Partie annuler", value="Désoler mais la partie de Garou a éter annuler.", inline=False)
                await self.bot.say(embed=embed)

            else:
                print("Commande lg stop lancer par: "+str(ctx.message.author)+" refuser car ce n'est pas le GM !")
                await self.bot.say(embed=self.erreur3)

    #Commande help
    @lg.command(pass_context=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Garou", description="Aide", color=0xff0000)
        embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
        embed.add_field(name="start", value="Lancement de la partie", inline=True)
        embed.add_field(name="join", value="Rejoidre la partie", inline=True)
        embed.add_field(name="play", value="Demarre la partie", inline=True)
        embed.add_field(name="stop", value="Termine la partie", inline=True)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Garou(bot))
    print("Garou charger")
