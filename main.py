import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from aiohttp import web
import asyncio

# Charger les variables d'environnement
load_dotenv()

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration du serveur web
app = web.Application()

async def handle_health_check(request):
    return web.Response(text="Bot is running!", status=200)

app.router.add_get('/', handle_health_check)

# Fonction pour lancer le serveur web
async def start_webserver():
    port = int(os.getenv('PORT', 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Serveur web démarré sur le port {port}")

# Événement quand le bot est prêt
@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Lire Tougen Anki"))
    await start_webserver()

# Événement pour la mise à jour des rôles
@bot.event
async def on_member_update(before, after):
    # ID du rôle à surveiller
    role_id = 1326778962143215677
    # ID du canal pour les messages
    channel_id = 1326229582273314937
    
    # Obtenir le canal
    channel = bot.get_channel(channel_id)
    if not channel:
        return
    
    # Vérifier si le rôle a été ajouté
    role = after.guild.get_role(role_id)
    if not role:
        return
        
    # Si le rôle a été ajouté
    if role not in before.roles and role in after.roles:
        await channel.send(f"Bienvenue dans la communauté de {role.name} <@{after.id}> ! 🎉")
    
    # Si le rôle a été retiré
    elif role in before.roles and role not in after.roles:
        await channel.send(f"Au revoir {after.name}, vous avez quitté la communauté de {role.name} 👋")

# Lancer le bot avec asyncio
async def main():
    async with bot:
        await bot.start(os.getenv('TOKEN'))

# Point d'entrée principal
if __name__ == "__main__":
    asyncio.run(main())
