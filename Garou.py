import json
import discord
import random
from random import randint
from discord.ext import commands
#from threading import Thread


class Garou:
    def __init__(self, bot):
        self.bot = bot
        self.discord = discord

        with open('config.json') as json_data_file:
            self.parameter = json.load(json_data_file)
        
        self.owner = self.parameter['Perms']['Admin']

        #Truc utile
        self.server = self.bot.get_server("177396472294277120")
        self.garou_role = discord.utils.get(self.server.roles, name="Garou")
        self.mort_role = discord.utils.get(self.server.roles, name="Morts")

        #Get des channels.
        self.forum_channel = self.bot.get_channel("402067902469242900")
        self.Garou_channel = self.bot.get_channel("403500093380100106")
        self.soeur_channel = self.bot.get_channel("403518380017057792")
        self.morts_channel = self.bot.get_channel("403529180563767311")
        self.village_voice_channel = self.bot.get_channel("403519327426576384")

        #Permmision des channels:
        #Quand c'est la nuit
        self.perms_nuit_forum = discord.PermissionOverwrite()
        self.perms_nuit_forum.read_message_history = False
        self.perms_nuit_forum.send_messages = False
        self.perms_nuit_forum.read_messages = True

        self.perms_nuit_Garou = discord.PermissionOverwrite()
        self.perms_nuit_Garou.read_message_history = False
        self.perms_nuit_Garou.send_messages = True
        self.perms_nuit_Garou.read_messages = True
        
        self.perms_nuit_soeur = discord.PermissionOverwrite()
        self.perms_nuit_soeur.read_message_history = False
        self.perms_nuit_soeur.send_messages = True
        self.perms_nuit_soeur.read_messages = True


        #Quand c'est le jour
        self.perms_jour_forum = discord.PermissionOverwrite()
        self.perms_jour_forum.read_message_history = False
        self.perms_jour_forum.send_messages = True
        self.perms_jour_forum.read_messages = True

        self.perms_jour_Garou = discord.PermissionOverwrite()
        self.perms_jour_Garou.read_message_history = False
        self.perms_jour_Garou.send_messages = False
        self.perms_jour_Garou.read_messages = True
        
        self.perms_jour_soeur = discord.PermissionOverwrite()
        self.perms_jour_soeur.read_message_history = False
        self.perms_jour_soeur.send_messages = False
        self.perms_jour_soeur.read_messages = True


    #Variables de base
    game = 0 #Dit si une partie est en cours et a quelle stade elle en est
    gm = () #Dit qui est le GM (ID)
    list_joueurs = [] #Dit qui sont les joueurs
    morts = [] #Dit qui sont les joueurs morts
    def_joueurs = dict() #Dit qui sont les joeurs defini avec leur roles
    random = [0] #Liste des chiffre random tiré
    num_joueurs = 0 #Nombre de joueurs dans la partie
    jour = 0 #C'est c'est le jour (1) ou la nuit (2), si c'est a 0 c'est que le jour n'est pas initialiser
    nuit = 1 #Compteur de nuit
    research = 0 #Quand le minimum de jouer est trouver
    num_morts = 0 #Le nombre de joueurs morts
    night_death = 0
    day_death = 0
    LG,VY,VO,SO,VG,CS,CU,CL,AG,MA,IL,IPDL,JDF,RE,GML,LGB,SA,AS,CER,MO,AC,SE,IDV,BE,ES,KZ,ISM = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 #Mise a zero des variables des roles

    #Vrai variables
    minijoueurs = 1 #5, Le nombre minimum de joueurs qu'il faut pour lancer une partie
    roles = ["0", "LG", "VY", "VO", "SO", "VG", "VG", "CS", "CU", "LG", "CL", "AG", "MA", "IL", "IPDL", "JDF", "VG", "RE", "GML", "VG", "LGB", "VG", "SA", "LG", "AS", "CER", "MO", "AC", "SE", "SE", "IDV", "BE", "ES", "KZ", "ISM", "VG"] #Les roles donner (0 est présant poue simplifier le code pendant l'attribution des roles)

#Tout le bordel de text et messages
    #Les introductions des roles
    def intro(self, role):
        intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
        intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
        if role == "VG":
            intro.add_field(name="Vous êtes : ", value="Villageois")
            intro.add_field(name="L'histoire :", value="*A Thiercelieu les habitants sont victimes d’une terrible malédiction, chaque jour ils tentent de tuer un loup-garou en votant*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous, à chaque journée, vous votez avec le reste des joueurs pour tenter d’éliminer les loups-garous.**", inline=False)
            return intro

        elif role == "LG":
            intro.add_field(name="Vous êtes : ", value="Loup-garou")
            intro.add_field(name="L'histoire :", value="*Le village de Thiercelieu est victime d’une terrible malédiction. Des loups-garous terrorisent les habitants de cette petite bourgade et dévorent les villageois.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les villageois. Chaque nuit, vous décidez, avec les autres loups-garous, de tuer une personne.**", inline=False)
            return intro

        elif role =="VY":
            intro.add_field(name="Vous êtes : ", value="Voyante")
            intro.add_field(name="L'histoire :", value="*Cette personne si secrète pourra-t-elle faire la lumière sur les évènements de Thiercelieu ? Ces dons bizarres pour la voyance lui permettent de connaitre la véritable nature des gens.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous pourrez connaitre le rôle d’une personne.**", inline=False)
            return intro

        elif role == "VO":
            intro.add_field(name="Vous êtes : ", value="Voleur")
            intro.add_field(name="L'histoire :", value="*Qui est donc ce chapardeur qui met la confusion dans la tête des gens ? Il n’est pas méchant, mais des gens disent qu’il manipulerait les autres.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Toutes les deux nuits, vous échangerez les rôles de deux personnes. **", inline=False)
            return intro

        elif role =="SO":
            intro.add_field(name="Vous êtes : ", value="Sorcière")
            intro.add_field(name="L'histoire :", value="*Quelle est cette femme qui concocte ses potions en secret, décidant du sort de ses victimes ? On la dit capable de soigner, mais aussi de tuer.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous pouvez soigner ou tuer une personne, ou ne rien faire. Attention, chaque potion ne peut être utilisé qu’une seule fois.**", inline=False)
            return intro

        elif role == "CS":
            intro.add_field(name="Vous êtes : ", value="Chasseur")
            intro.add_field(name="L'histoire :", value="*Cet homme seul à décider de prendre les armes et de traquer les loups-garous qui terrorisent le village. Qui sait ce que pourrait faire un homme armé au bord de la mort ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Si vous êtes tué, vous pourrez tuer une autre personne avant de mourir.**", inline=False)
            return intro

        elif role == "CU":
            intro.add_field(name="Vous êtes : ", value="Cupidon")
            intro.add_field(name="L'histoire :", value="*Qui recevra les flèches de l’amour lancées par ce petit être ? Ceux-ci se voueront un amour pur et total, et dépendrons l’un de l’autre.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. En début de partie, vous rendrez deux personnes amoureuses. Celles-ci seront dépendante l’une de l’autre, et si l’une meurt, l’autre se tuera de chagrin.**", inline=False)
            return intro

        elif role == "CL":
            intro.add_field(name="Vous êtes : ", value="Chien-loup")
            intro.add_field(name="L'histoire :", value="*Il existe à Thiercelieu une espèce de chien très rares, pouvant adopter des comportements violents. Deviendra-t-il loup-garou, ou restera t-il un chien docile ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**En début de partie vous aurez le choix entre rejoindre les loups-garous ou les villageois.**", inline=False)
            return intro

        elif role == "AG":
            intro.add_field(name="Vous êtes : ", value="Ange")
            intro.add_field(name="L'histoire :", value="*Ce petit homme volant ce fiche éperdument du sort d’un petit village perdu au fond des landes. Tout ce qu’il veut c’est s’envoler un retrouver le calme des cieux.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de gagner la partie seul. Si vous êtes tué par les villageois au premier jour, vous remportez la partie. Sinon, vous devenez simple villageois.**", inline=False)
            return intro

        elif role == "MA":
            intro.add_field(name="Vous êtes : ", value="Maire")
            intro.add_field(name="L'histoire :", value="*Tout village, même dans la terreur, a besoin d’un leader en qui avoir confiance.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Votre vote compte double.**", inline=False)
            return intro

        elif role == "IL":
            intro.add_field(name="Vous êtes : ", value="Illettré")
            intro.add_field(name="L'histoire :", value="*L’éducation est privilège dont tout le monde devrait avoir accès. Cette personne étrangère ne comprend rien aux paroles des autres habitants. De temps en temps il aime se balader la nuit, il voit des choses étranges, sans savoir ce qu’elles sont.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but et de tuer tous les loups-garous. Chaque nuit, vous percevez des morceaux de la conversation des loups-garous.**", inline=False)
            return intro

        elif role == "IPDL":
            intro.add_field(name="Vous êtes : ", value="Infect père des loups")
            intro.add_field(name="L'histoire :", value="*Même les loups-garous ont une famille. Cette famille-là est ancienne est terrible, capable de pervertir le cœur des plus nobles.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les villageois. Une fois par partie, vous pouvez infecter une personne désignée comme victime par les loups-garous. Celle-ci ne sera pas tuée mais deviendra secrètement un loup-garou.**", inline=False)
            return intro

        elif role == "JDF":
            intro.add_field(name="Vous êtes : ", value="Joueur de flûte")
            intro.add_field(name="L'histoire :", value="*Cet homme, autrefois banni, et aujourd’hui oublié, revient au village pour se venger. Armé de sa flûte à bec, il prend peu à peu possession du village à qui il souhaite donner une leçon.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de contaminer tous les habitants du village. Chaque nuit, vous contaminez une ou deux personnes.**", inline=False)
            return intro

        elif role == "RE":
            intro.add_field(name="Vous êtes : ", value="Renard")
            intro.add_field(name="L'histoire :", value="*Les loups ne sont pas les seuls animaux à Thiercelieu. Ce renard rusé serait capable de sentir l’âme des gens ainsi que leurs intentions.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous voyez le rôle de trois personnes, mais si aucune d’elles n’est un loup-garou, vous perdez votre pouvoir.**", inline=False)
            return intro

        elif role == "GML":
            intro.add_field(name="Vous êtes : ", value="Grand méchant loup")
            intro.add_field(name="L'histoire :", value="*Il n’y a pas que les trois petits cochons qui craignent le grand méchant loup. Celui est encore plus meurtrier est assoiffé de sang que ses semblables.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les villageois. Tant qu’aucun loup-garou n’est mort, vous pouvez tuer une personne supplémentaire par nuit.**", inline=False)
            return intro

        elif role == "LGB":
            intro.add_field(name="Vous êtes : ", value="Loup-garou blanc")
            intro.add_field(name="L'histoire :", value="*Il y aurait un traitre dans les rangs des loups-garous. Celui-ci les éliminerait de l’intérieur, un à un.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de finir la partie seul. Toutes les deux nuits, vous pouvez tuer un loup-garou, en plus de la victime de chaque nuit.**", inline=False)
            return intro

        elif role == "SA":
            intro.add_field(name="Vous êtes : ", value="Salvateur")
            intro.add_field(name="L'histoire :", value="*A Thiercelieu, ce personnage est devenu une légende. Sa bénédiction permettrait de se protéger des événements récents.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, vous accordez votre bénédiction à une personne. Celle-ci ne pourra pas être tuée pendant la nuit.**", inline=False)
            return intro

        elif role == "AS":
            intro.add_field(name="Vous êtes : ", value="Assassin")
            intro.add_field(name="L'histoire :", value="*A Thiercelieu, il y a un fou qui n’avait jusque-là jamais été dangereux. Mais les récents évènements ont perturbé sa santé mentale. Depuis, il vit dans une folie meurtrière qui ne peut contrôler.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de finir la partie seul. Chaque matin, vous tuez une personne au hasard.**", inline=False)
            return intro

        elif role == "CER":
            intro.add_field(name="Vous êtes : ", value="Chevalier à l’épée rouillée")
            intro.add_field(name="L'histoire :", value="*Don Quigrince était un fier chevalier vaillant ayant participé à de nombreuses batailles. Aujourd’hui, le temps et le manque d’action se sont transformés en ennui. Il ne mange plus, dors peu, et ne s’est pas occupé de son épée depuis fort longtemps. Celle-ci s’est émoussée, et pourrait surement empoissonner un loup trop gourmand.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Si vous êtes tué par les loup-garou, celui qui avait proposé votre mort sera tué la nuit suivante.**", inline=False)
            return intro

        elif role == "MO":
            intro.add_field(name="Vous êtes : ", value="Montreur d’ours")
            intro.add_field(name="L'histoire :", value="*En plus des loups-garous, il y a un ours qui rode dans les bois de Thiercelieu. Celui-ci est très grincheux, et n’hésitera pas à grogner pour effrayer les loups-garous trop curieux.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Chaque nuit, si un loup-garou se trouve à coté de vous, vous grognez.**", inline=False)
            return intro

        elif role == "AC":
            intro.add_field(name="Vous êtes : ", value="Ancien")
            intro.add_field(name="L'histoire :", value="*L’expérience amène la sagesse. Et la sagesse amène la maitrise de soi. Le doyen du village l’a bien compris. Bien qu’étant d’un âge avancé, il saura s’enfuir face aux loups-garous qui essayeraient de le tuer. Cependant, sa mort démoraliserait tous les villageois.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer les loups-garous. Si vous êtes tué par les loups garous, vous pourrez échanger votre rôle avec une personne au hasard la nuit suivante. Si vous êtes tué une deuxième fois, tous les villageois restants perdrons leurs pouvoirs.**", inline=False)
            return intro

        elif role == "SE":
            intro.add_field(name="Vous êtes : ", value="Sœur")
            intro.add_field(name="L'histoire :", value="*Rien n’est plus beau que la fraternité. Ces deux sœurs sont comme deux doigts d’une même main, ou deux cheveux d’une même mèche. Elles se comprennent sans même se parler.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les villageois. Certaines nuits, vous serez appelés, et pourrait communiquer avec l’autre sœur.**", inline=False)
            return intro

        elif role == "IDV":
            intro.add_field(name="Vous êtes : ", value="Idiot du village")
            intro.add_field(name="L'histoire :", value="*Les villageois ont beau essayer d’en faire quelque chose, il ne comprend rien de rien. Cependant, ils ne pourront jamais lui faire de mal. Même au moment de le tuer, ils décideront de ne rien lui faire, et de ne plus lui parler. Qui écouterait un idiot ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Si vous êtes tué par les villageois, vous serez acquitté mais perdrez votre droit de vote.**", inline=False)
            return intro

        elif role == "ES":
            intro.add_field(name="Vous êtes : ", value="Enfant sauvage")
            intro.add_field(name="L'histoire :", value="*Cet enfant est sorti de la forêt un jour, sans prévenir. Il a été élevé par les loups, dans les bois. Cependant, il essaye de s’intégrer dans le village, en prenant un modèle. Qui sait ce qu’il pourrait devenir s’il lui arrivait quelque chose ?*", inline=False)
            intro.add_field(name="Votre bute : ", value="**En début de partie, vous choisissez un modèle. Tant que cette personne est en vie, vous restez villageois, mais si elle meurt, vous vous transformez en loup-garou.**", inline=False)
            return intro

        elif role == "BE":
            intro.add_field(name="Vous êtes : ", value="Bouc-émissaire")
            intro.add_field(name="L'histoire :", value="*Qu’est-ce que cet homme a bien pu faire pour être autant détester par le village ? En cas de doute, c’est toujours de sa faute.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups-garous. Si les villageois doutent sur qui tuer pendant le vote, vous serez tué par défaut.**", inline=False)
            return intro

        elif role == "KZ":
            intro.add_field(name="Vous êtes : ", value="Kamikaze")
            intro.add_field(name="L'histoire :", value="*Cet homme au passif si tumultueux n’a plus rien à perdre. Il serait prêt à risquer sa vie pour faire entendre raison aux autres villageois.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups garous. Une fois par partie, vous pouvez à tout moment tuer une autre personne, mais vous mourrez en faisant cela.**", inline=False)
            return intro

        elif role == "ISM":
            intro.add_field(name="Vous êtes : ", value="Insomniaque")
            intro.add_field(name="L'histoire :", value="*Les problèmes de sommeil sont terribles. Mais cela permet de savoir tout avant les autres. Impossible de savoir ce qui empêche cette femme de dormir. Peut-être ce qu’elle apprend le matin, à l’aube.*", inline=False)
            intro.add_field(name="Votre bute : ", value="**Votre but est de tuer tous les loups –garous. Toutes les nuits, vous saurez le dérouler exact de tout la nuit.**", inline=False)
            return intro

    #Le nom des roles selon leur abrevation
    def get_role_name(self, role):
        intro=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
        intro.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
        if role == "VG":
            name = "Villageois"
            return name

        elif role == "LG":
            name = "Loup-garou"
            return name

        elif role =="VY":
            name = "Voyante"
            return name

        elif role == "VO":
            name = "Voleur"
            return name

        elif role =="SO":
            name = "Sorcière"
            return name

        elif role == "CS":
            name = "Chasseur"
            return name

        elif role == "CU":
            name = "Cupidon"
            return name

        elif role == "CL":
            name = "Chien-loup"
            return name

        elif role == "AG":
            name = "Ange"
            return name

        elif role == "MA":
            name = "Maire"
            return name

        elif role == "IL":
            name = "Illettré"
            return name

        elif role == "IPDL":
            name = "Infect père des loups"
            return name

        elif role == "JDF":
            name = "Joueur de flûte"
            return name

        elif role == "RE":
            name = "Renard"
            return name

        elif role == "GML":
            name = "Grand méchant loup"
            return name

        elif role == "LGB":
            name = "Loup-garou blanc"
            return name

        elif role == "SA":
            name = "Salvateur"
            return name

        elif role == "AS":
            name = "Assassin"
            return name

        elif role == "CER":
            name = "Chevalier à l’épée rouillée"
            return name

        elif role == "MO":
            name = "Montreur d’ours"
            return name

        elif role == "AC":
            name = "Ancien"
            return name

        elif role == "SE":
            name = "Sœur"
            return intro

        elif role == "IDV":
            name = "Idiot du village"
            return name

        elif role == "ES":
            name = "Enfant sauvage"
            return name

        elif role == "BE":
            name = "Bouc-émissaire"
            return name

        elif role == "KZ":
            name = "Kamikaze"
            return name

        elif role == "ISM":
            name = "Insomniaque"
            return name


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

    #Message de début de nuit
    soir=discord.Embed(title="Garou", description="Le temps qui passe", color=0xff0000)
    soir.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
    soir.add_field(name="Soir", value="La nuit tombe sur Thiercelieu tout au tant que l'inquietude sur ses habitants", inline=False)

    #Message de début de jour
    day=discord.Embed(title="Garou", description="Le temps qui passe", color=0xff0000)
    day.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
    day.add_field(name="Jour", value="Le jour se lève sur Thiercelieu !", inline=False)


    #Pour verifier que la personne donner soit bien un joueur
    def is_joueurs(self, target):
        if target in self.def_joueurs:
            return True
        return False

    #Routine a chaque nuit
    async def night_start(self):
        
        #Envoie du message de nuit
        await self.bot.send_message(self.forum_channel, embed=self.soir)
        await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit sur Thiercelieu"))

        #Definition des permission du channel general
        await self.bot.edit_channel_permissions(self.forum_channel, self.garou_role, self.perms_nuit_forum)
        for j in self.list_joueurs:
            await self.bot.server_voice_state(j, mute=True, deafen=False)


        #print(list(self.def_joueurs.keys())[list(self.def_joueurs.values()).index("LG")])

        #On vérifie si c'est la première nuit
        if self.jour == 0:
            if "SA" in self.def_joueurs.values():
                if self.SA == 0:
                    #Tour du SA (Salvateur)
                    print("Tour du Salvateur")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour du Salvateur"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour du Salvateur", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.SA = 1
                    return None
            
            if "CU" in self.def_joueurs.values():
                if self.CU == 0:
                    #Tour de Cupidon
                    print("Tour de Cupidon")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour de Cupidon"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour de Cupidon", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.CU = 1
                    return None

                if self.CU == 2:
                    #Amoureux se rencontre
                    print("Amoureux se rencontre")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour des amoureux"))
                    
                    self.CU == 3
                    return None
            
            if "SE" in self.def_joueurs.values():
                if self.SE == 0:
                    #Tour des Sœur
                    print("Tour des Sœur")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour des Soeur"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour des Soeurs", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)


                    for j, r in self.def_joueurs.items():
                        if r == "SE":
                            await self.bot.edit_channel_permissions(self.soeur_channel, j, self.perms_nuit_soeur)

                    self.SE = 1
                    return None

            if "CL" in self.def_joueurs.values():
                if self.CL == 0:
                    #Tour du Chien-loup
                    print("Tour du Chien-loup")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour du Chien-loup"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour du Chien-loup", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.CL = 1
                    return None

            if "ES" in self.def_joueurs.values():
                if self.ES == 0:
                    #Tour de l'Enfant sauvage
                    print("Tour de l'Enfant sauvage")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour de l'Enfant sauvage"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour de l'Enfant sauvage", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.ES = 1
                    return None

            if "VY" in self.def_joueurs.values():
                if self.VY == 0:
                    #Tour de la voyante
                    print("Tour de la voyante")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour de la voyante"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour de la voyante", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.VY = 1
                    return None

            if "RE" in self.def_joueurs.values():
                if self.RE == 0:
                    #Tour du Renard (le plus chiant je pense)
                    Print("Tour du Renard")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour du Renard"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour du Renard", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.RE = 1
                    return None

            if "LG" in self.def_joueurs.values():
                if self.LG == 0:
                    #Tour des Loups-Garou
                    print("Tour des Loups-Garou")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour des Loups-Garou"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour des Loups-Garou", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    for j, r in self.def_joueurs.items():
                        if r == "LG":
                            await self.bot.edit_channel_permissions(self.Garou_channel, j, self.perms_nuit_Garou)
                            print("Perms garou")

                    loup=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    loup.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    loup.add_field(name="Vote", value="Les votes sont ouvert pour chosir qui tuer ce soir !", inline=False)
                    loup.add_field(name="Victime", value="")

                    
                    self.LG = 1
                    return None

            if "GML" in self.def_joueurs.values():
                if self.GML == 0:
                    #Tour du Grand Mechant Loup
                    print("Tour du Grand Mechant Loup")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour du Grand Mechant Loup"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour du Grand Mechant Loup", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.GML = 1
                    return None
            
            if "SO" in self.def_joueurs.values():
                if self.SO == 0:
                    #Tour de la Sorcière
                    print("Tour de la Sorcière")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour de la Sorcière"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour de la Sorcière", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.SO = 1
                    return None
            
            if "AS" in self.def_joueurs.values():
                if self.AS == 0:
                    #Tour de l'Assassin
                    print("Tour de l'Assassin")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour de l'Assassin"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour de l'Assassin", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.AS = 1
                    return None

            if "JDF" in self.def_joueurs.values():
                if self.JDF == 0:
                    #Tour du Joueur de flûte
                    print("Tour du Joueur de flûte")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour du Joueur de flùte"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour du Jouer de flùte", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.JDF = 1
                    return None

            if "ISM" in self.def_joueurs.values():
                if self.ISM == 0:
                    #Tour de l'Insomniaque
                    print("Tour de l'Insomniaque")
                    await self.bot.change_presence(game=discord.Game(name="LG: c'est la nuit, tour de l'Insomniaque"))
                    vote=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
                    vote.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    vote.add_field(name="Vote", value="C'est le tour de l'Insomniaque", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=vote)

                    self.ISM = 1
                    return None

        #Nuit normal
        elif self.jour == 2:
            #if
            return None
        
        #Gestion des morts
        if night_death == 0:
            await self.death()
        
        self.night_death = 0

        #Action de fin de nuit
        print("Fin de la nuit")

        #Fin de la nuit
        #On compte le nombre de soir
        self.nuit = self.nuit+1

        #On reset l'ordre de passage des roles
        LG,VY,VO,SO,VG,CS,CU,CL,AG,MA,IL,IPDL,JDF,RE,GML,LGB,SA,AS,CER,MO,AC,SE,IDV,BE,ES,KZ,ISM, = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 #Mise a zero des variables des roles

        self.jour = 1
        await self.day_start()

    print("Erreure Nuit")

    async def day_start(self):
        #Début des actions selon les roles
        print("Jour")
        await self.bot.send_message(self.forum_channel, embed=self.day)
        await self.bot.edit_channel_permissions(self.forum_channel, self.garou_role, self.perms_jour_forum)
        await self.bot.change_presence(game=discord.Game(name="LG: c'est le jour"))

        for j, r in self.def_joueurs:
            if r != "Mort":
                await self.bot.server_voice_state(j, mute=False, deafen=False)
    
    async def death(self):
        if self.morts != []:
            mort=discord.Embed(title="Garou", description="Nuit", color=0xff0000)
            mort.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            for j in self.morts:
                self.num_joueurs = self.num_joueurs+1
                role = self.def_joueurs[j]
                self.def_joueurs[j] = "Mort"
                await self.bot.add_roles(j, self.mort_role)
                mort.add_field(name="Morts", value="@"+str(j)+" est mort(e) ce soir ! \nCetait un(e) "+str(self.get_role_name(role))+" !", inline=False)
            await self.bot.send_message(self.forum_channel, embed=mort)
            self.morts = list()
            
            #Gestion du retour
            if self.jour == 1:
                if self.day_death == 0:
                    self.day_death = 1
                    await self.day_start()
                    
            elif self.jour == 2:
                if self.night_death == 0:
                    self.night_death = 1
                    await self.day_start()
            
            elif self.jour == 0:
                if self.night_death == 0:
                    self.night_death = 1
                    await self.day_start()
            
            return True


    #Quand la partie prend fin
    async def end(self):
        print("Reset des roles")

        #Demute des joueurs
        for j in self.list_joueurs:
            await self.bot.server_voice_state(j, mute=False, deafen=False)
            await self.bot.remove_roles(j, self.garou_role)
            await self.bot.remove_roles(j, self.mort_role)
            await self.bot.move_member(j, self.bot.get_channel("387724490483695627"))

        #Suppresion des attribution spetiale des loups-garou
        for j, r in self.def_joueurs.items():
            if r == "LG":
                await self.bot.delete_channel_permissions(self.Garou_channel, j)

        #Supression des attribution spetial des soeurs
        for j, r in self.def_joueurs.items():
            if r == "SE":
                await self.bot.delete_channel_permissions(self.soeur_channel, j)

        await self.bot.edit_channel_permissions(self.forum_channel, self.garou_role, self.perms_nuit_forum)

        #Remise a zero du statu du bot
        await self.bot.change_presence(game=discord.Game(name=self.parameter['Bot']['statu']))

        #Reset des variables
        print("Reset des variables")
        

        #Marche pas :/
        #await self.bot.change_presence(self.save_game) #Reset du statu

        #Reboot de l'ext
        self.bot.unload_extension("Garou")
        self.bot.load_extension("Garou")

    #Définition du groupe de commande lg
    @commands.group(pass_context=True)
    async def lg(self, ctx):
        if ctx.invoked_subcommand is None:
            #Affiche le help au cas ou de commande vide ou incorrecte
            await ctx.invoke(self.help)


    #Commande pour démarre le jeux
    @lg.command(pass_context=True)
    async def start(self, ctx):
        if self.game >= 1: #Verification si une partie est deja lancer
            print("Commande lg start lancer par: "+str(ctx.message.author)+" refuser, partie deja lancer")
            await self.bot.say(embed=self.erreur1)

        else:
            print("Commande lg start lancer par: "+str(ctx.message.author))
            self.game=1 #On dit qu'une la partie est lancer
            self.gm=ctx.message.author #On defini le GM
            self.list_joueurs.insert(0, ctx.message.author) #On ajoute le GM dans la liste de joueurs
            embed=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
            embed.add_field(name="Début de partie", value="Une partie a été lancer par: "+str(ctx.message.author)+" ! \nPour rejoindre, taper la commande: ```lg join```", inline=False)
            await self.bot.say(embed=embed)
            self.research = 1
                


    #Commande pour rejoindre la partie
    @lg.command(pass_context=True)
    async def join(self, ctx):
        if self.game == 0: #Verification si une partie est deja lancer
            print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        elif self.game == 2:
            print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, joueurs deja defini !")
            await self.bot.say(embed=self.erreur1)

        elif self.game == 1:
            if self.gm == ctx.message.author: #Verification si c'est le GM
                print("Commande lg join lancer par: "+str(ctx.message.author)+" refuser, c'est le GM !")
                embed=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                embed.add_field(name="Imposible", value="Désoler mais vous êtes le GM, vous avez deja rejoint par defaut.", inline=False)
                await self.bot.say(embed=embed)

            else:
                print("Commande lg join lancer par: "+str(ctx.message.author))
                self.list_joueurs.append(ctx.message.author)
                await self.bot.change_presence(game=discord.Game(name='LG: actuellement '+str(len(self.list_joueurs))+' habitants a Thiercelieu'))
                embed=discord.Embed(title="Garou", description="Dèmarrage", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                embed.add_field(name="Début de partie", value=str(ctx.message.author)+" a rejoint !", inline=False)
                await self.bot.say(embed=embed)

                if len(self.list_joueurs) >= self.minijoueurs:
                    if self.research == 1:
                        print("Nombre de joueurs sufissant")
                        embed=discord.Embed(title="Garou", description="Démarrage", color=0xff0000)
                        embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                        embed.add_field(name="Début de partie", value="Il y a "+str(len(self.list_joueurs))+" joueurs dans la partie, cela est le nombre minimale. \nTaper: ```lg play``` si vous voullez commencer la partie !", inline=False)
                        await self.bot.say(embed=embed)
                        self.research = 0


    #Commande pour lancer la partie
    @lg.command(pass_context=True)
    async def play(self, ctx):
        if self.game == 0: #Verification si une partie est deja lancer
            print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        elif self.game == 2:
            print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, joueurs deja defini !")
            await self.bot.say(embed=self.erreur1)

        elif self.game == 1:
            if self.gm == ctx.message.author: #Verification si c'est le GM
                if len(self.list_joueurs) < self.minijoueurs: #Verification du nombre de joueurs minimal requi
                    print("Commande lg play lancer par: "+str(ctx.message.author)+", refuser car minimum de joueurs pas atteint")
                    embed=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
                    embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    embed.add_field(name="Imposible", value="Désoler mais il n'y a que "+str(len(self.list_joueurs))+" joueur(s) dans la partie", inline=False)
                    await self.bot.say(embed=embed)

                else:
                    self.game=2 #On dit que les joueurs sont defini
                    self.num_joueurs=len(self.list_joueurs) #On defini combien de joueurs en tout
                    
                    print("Commande lg play lancer par: "+str(ctx.message.author)) #On log
                    await self.bot.change_presence(game=discord.Game(name='LG: definition des roles..."'))

                    #Definition des roles
                    for j in range(0,self.num_joueurs): #Un boucle qui fait autent de fois qu'il y a de joueurs
                        target = self.list_joueurs[j] #Prend dans la liste des joueurs le joueur en question.
                        while self.is_joueurs(target) != True: #Boucle tant que le jouer n'est pas dans la liste des personnes défini
                            r = randint(1,self.num_joueurs) #Tire un chiffre random entre 1 et le nombre de jouers
                            if r not in self.random: #Si se chiffre a deja éter tiré, alors sela relance le while
                                self.random.append(r) #Ajoute le chiffre random dans la liste des chiffres deja tiré

                                #On verifie la possibiliter d'avoir les soeurs
                                if self.roles[r] == "SE":
                                    if self.num_joueurs <= 28:
                                        self.r = self.r+2

                                self.def_joueurs[target] = self.roles[r] #Ajoute dans le dico le joueur et assigne son role grace au chiffre random
                                

                                #Envoie du message de role
                                embed = self.intro(self.roles[r])
                                await self.bot.send_message(target, embed=embed)
                                print(self.def_joueurs) #On log les roles

                                #Ajout du role
                                await self.bot.add_roles(target, self.garou_role)

                                #Deplacement de la personne
                                await self.bot.move_member(target, self.village_voice_channel)

                    #Envoie du message de dèmmarage
                    embed=discord.Embed(title="Garou", description="Démarrage", color=0xff0000)
                    embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    embed.add_field(name="Début de partie", value="Definitions de joueurs terminer ! \nIl y a "+str(self.num_joueurs)+" joueurs dans la partie. \nDefinitions du role de chacun des joueurs en cours, ils vous seront envoyer par MP !", inline=False)
                    await self.bot.say(embed=embed)

                    #Gestion du message du bot
                    #self.save_game = discord.Game
                    #await self.bot.change_presence(game=discord.Game(name='Garou avec '+str(self.num_joueurs)+' habitants a Thiercelieu'))

                    #Gestion des permissions de base
                    await self.bot.edit_channel_permissions(self.forum_channel, self.garou_role, self.perms_nuit_forum)
                    
                    #Envoie du message du début
                    embed=discord.Embed(title="Garou", description="Démarrage", color=0xff0000)
                    embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                    embed.add_field(name="Début de partie", value="Bienvenue dans la partie de Garou ! \nIl y a "+str(self.num_joueurs)+" habitants a Thiercelieu pour le moment. \nBonne chance !", inline=False)
                    await self.bot.send_message(self.forum_channel, embed=embed)
                    
                    #On commence la nuit
                    await self.night_start()

            else:
                print("Commande lg play lancer par: "+str(ctx.message.author)+" refuser, pas le GM !")
                await self.bot.say(embed=self.erreur3)

    @lg.command(pass_context=True)
    async def test(self, ctx):
        self.morts.append(ctx.message.author) #Pour le test

        await self.death()
        
        

    @lg.command(pass_context=True)
    async def vote(self, ctx):
        if self.game == 0: #Verification si une partie est deja lancer
            print("Commande lg vote lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        elif self.game == 1:
            print("Commande lg vote lancer par: "+str(ctx.message.author)+" refuser, definition des joueurs non lancer !")
            await self.bot.say(embed=self.erreur1)

        elif self.game == 2:
            if self.is_joueurs(ctx.message.author) == True:
                for j, r in self.def_joueurs.items():
                    if r == "SA":
                        if self.SA == 1:
                            #Vote du Salvateur
                            print("Vote du Salvateur")

                            self.SA = 2

                    elif r == "LG":
                        if self.LG == 1:
                            #Vote des loup Garous
                            print("Vote des loups-garou")

                            #Faut faire le system de vote et aprés cela 
                            #self.LG = 2


                    elif r == "VY":
                        if self.VY == 1:
                            #Vote de la voyante
                            print("Vote de la voyante")

                        else :
                            await self.bot.say("Désoler mais c'est pas a vous !")

            else:
                print("Pas jouer")

    #Commande pour annuler le Garou
    @lg.command(pass_context=True)
    async def stop(self, ctx):
        if self.game == 0:
            print("Commande lg stop lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        elif self.game >= 1:
            if self.gm == ctx.message.author:
                print("Commande lg stop lancer par: "+str(ctx.message.author))
                embed=discord.Embed(title="Garou", description="Attention", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                embed.add_field(name="Partie annuler", value="Désoler mais la partie de Garou a éter annuler.", inline=False)
                await self.bot.say(embed=embed)

                await self.end() #Séquance de fin

            else:
                print("Commande lg stop lancer par: "+str(ctx.message.author)+" refuser car ce n'est pas le GM !")
                await self.bot.say(embed=self.erreur3)

    @lg.command(pass_context=True)
    async def forcestop(self, ctx):
        if self.game == 0:
            print("Commande lg force-stop lancer par: "+str(ctx.message.author)+" refuser, aucune partie lancer !")
            await self.bot.say(embed=self.erreur2)

        elif self.game >= 1:
            if ctx.message.author.id in self.owner:
                print("Commande lg force-stop lancer par: "+str(ctx.message.author))
                embed=discord.Embed(title="Garou", description="Attention", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                embed.add_field(name="Partie annuler de force", value="Désoler mais la partie de Garou a éter annuler par la force !", inline=False)
                await self.bot.say(embed=embed)

                await self.end(ctx) #Séquance de fin

            else:
                print("Commande lg force-stop lancer par: "+str(ctx.message.author)+" refuser car ce n'est pas un Admin !")
                erreur=discord.Embed(title="Garou", description="Erreur", color=0xff0000)
                erreur.set_thumbnail(url="https://i.imgur.com/XLPDenM.png")
                erreur.add_field(name="Imposible", value="Désoler mais vous n'étes pas Admin  !", inline=False)
                await self.bot.say(embed=erreur)

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
