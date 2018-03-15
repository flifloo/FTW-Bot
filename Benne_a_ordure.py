import discord
from discord.ext import commands

    #Paramètres

deletion_minimal = -2       #quantité de votes totale nécessaire
                            #pour supprimer un post.
                            #Prends en compte le nombre de votes
                            #pour le conserver et pour le supprimer.
delet_symbole = "🗑"   #Réaction permettant la suppression du post.
cons_symbole = "♻"    #Réaction permettant la conservation du post.

authorized_to_start_deletion = ["156484695083843585","177393521051959306"]
blocked_from_deleted = [".156484695083843585",".384104235375001632"]

reactDict = {}
messageDict = {}

def authorized_verif(id):
    for i in range(len(authorized_to_start_deletion)):
        if id == authorized_to_start_deletion[i]:
            return True
    return False

def anti_delete(id):
    for i in range(len(blocked_from_deleted)):
        if str(id) == blocked_from_deleted[i]:
            return False
    return True


async def first_reaction(self , reaction , user):
    if authorized_verif(user.id):
        print("Création")
        if reaction.emoji == delet_symbole:
            reactDict[reaction.message.id]=-1
        elif reaction.emoji == cons_symbole:
            reactDict[reaction.message.id]=1
        date,heure = timeCorrect(reaction.message.timestamp)

        message = str(reaction.message.author.mention)+" a reçu un vote pour la suppression ou la conservation de son message du "+str(reaction.message.timestamp)+".Si vous souhaitez voir son message supprimé, votez "+delet_symbole+". Si vous pensez que son message est correct, votez "+str(cons_symbole)+"."
        m = await self.bot.send_message(reaction.message.channel,message)
        messageDict[reaction.message.id]=m
        await self.bot.add_reaction(reaction.message,cons_symbole)
        await self.bot.add_reaction(reaction.message,delet_symbole)

async def delete(self , reaction , user):
    await self.bot.delete_message(reaction.message)
    await self.bot.delete_message(messageDict[reaction.message.id])

def timeCorrect(temps):
    date = "5"
    heure = "6"
    return date,heure

class Ben:
    def __init__(self,bot):
        self.bot = bot
        f = open("log_test.txt","a")    #Montres le début de l'enregistrement dans les logs.
        f.write("\nDébut de l'enregistrement des réactions.\n")
        f.close


    async def on_reaction_remove(self,reaction,user):#Récupères la réaction
        print("-"+str(reaction.emoji))  #si on retire une réaction.
        print(reaction.count)
        print(user.name)
        print(reaction.message.id)
        if str(reaction.emoji) == cons_symbole:  #Vérifie si le caractère
            reactDict[reaction.message.id]-=1  #corresponds au symbole
        elif str(reaction.emoji) == delet_symbole:   #de suppression
            reactDict[reaction.message.id]+=1
                                                 #ou au symbole de conservation.
        print("num = "+str(reactDict[reaction.message.id]))
        if reactDict[reaction.message.id]==deletion_minimal:
            await delete(self , reaction , user)                  #si le
                                                                #nombre est
                                                                #suppérieur,
                                                                #suppression.




    #def auto_deletion(self,Message):
    #    await self.bot.delete_message(Message)
    #    print(Message.content)



    async def on_reaction_add(self, reaction, user): #Récupères la réaction
        print("+"+str(reaction.emoji))      #si on ajoute une réaction.
        print(reaction.count)
        print(user.name)
        print(reaction.message.id)
        if anti_delete(reaction.message.author.id)== True:
            print("Message autorisé")
            if str(reaction.emoji) == cons_symbole:
                if reactDict.get(reaction.message.id)!=None:
                    reactDict[reaction.message.id]+=1
                    print("Message présent")
                else:
                    await first_reaction(self,reaction,user)



            if str(reaction.emoji) == delet_symbole:
                if reactDict.get(reaction.message.id)!=None:
                    reactDict[reaction.message.id]-=1
                    print("Message présent")
                else:
                    await first_reaction(self,reaction,user)



            if reactDict.get(reaction.message.id) != None :
                if reactDict[reaction.message.id]<=deletion_minimal:
                    await delete(self , reaction , user)
                else:
                    print(reactDict[reaction.message.id])

            #print("tzdsqdzqs"+str(reactDict[reaction.message.id]))

def setup(bot):
    bot.add_cog(Ben(bot))
    print("Benne_a_ordure chargée")
