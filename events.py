import discord
from config import ROLE_TOUGEN_ANKI_ID, WELCOME_THREAD_ID

async def setup(bot):
    @bot.event
    async def on_ready():
        print(f'Bot connecté en tant que {bot.user.name}')
        await bot.change_presence(activity=discord.Game(name="Lire Tougen Anki"))
        from utils import start_webserver
        await start_webserver(bot)

    @bot.event
    async def on_member_update(before, after):
        try:
            # Obtenir le fil (thread)
            thread = await bot.fetch_channel(WELCOME_THREAD_ID)
            if not thread:
                print(f"Fil {WELCOME_THREAD_ID} non trouvé")
                return
            
            # Vérifier si le rôle a été ajouté
            role = after.guild.get_role(ROLE_TOUGEN_ANKI_ID)
            if not role:
                print(f"Rôle {ROLE_TOUGEN_ANKI_ID} non trouvé")
                return
                
            # Si le rôle a été ajouté
            if role not in before.roles and role in after.roles:
                await thread.send(f"Bienvenue dans la communauté de {role.name} <@{after.id}> ! 🎉")
                print(f"Rôle ajouté pour {after.name}")
            
            # Si le rôle a été retiré
            elif role in before.roles and role not in after.roles:
                await thread.send(f"Au revoir {after.name}, vous avez quitté la communauté de {role.name} 👋")
                print(f"Rôle retiré pour {after.name}")
                
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {str(e)}")