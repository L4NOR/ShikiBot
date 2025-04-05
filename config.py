import os
from dotenv import load_dotenv
import discord

# Charger les variables d'environnement
load_dotenv()

# Configuration du bot
BOT_TOKEN = os.getenv('TOKEN')
PORT = int(os.getenv('PORT', 8080))
COMMAND_PREFIX = '!'

# ID des rôles et canaux
ROLE_TOUGEN_ANKI_ID = 1326778962143215677
WELCOME_THREAD_ID = 1330144191816142941
ANNOUNCEMENTS_CHANNEL_ID = 1326213946188890142 
TWITTER_TOUGEN_CHANNEL_ID=1330144528077946960
DISCUSSIONS_CATEGORY_ID = 1326230010608226364

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Couleurs pour les embeds
PINK_COLOR = 0xFF1493
ROYAL_BLUE_COLOR = 0x1E90FF

# Réactions pour les annonces
ANNOUNCEMENT_REACTIONS = ["🔥", "👀", "❤️"]

# Paramètres pour les threads de discussion
THREAD_AUTO_ARCHIVE_DURATION = 1440  # 24 heures

# Configuration de l'API Twitter
TWITTER_API_KEY = "4RaKtzkT8k7HbNBT6aLXMo5Cv"
TWITTER_API_SECRET = "3j9GtwbFiVvMw5lxH71s0dggaMia7LPKOKOaPoY7V8CogDkFz6"
TWITTER_ACCESS_TOKEN = "1282370735672037379-bQSSjJ4piOsG7WBEMFxxuQg4sp1rxE"
TWITTER_ACCESS_SECRET = "LZJdTpx0nQ6RwgR2ljF3rFrgXdz3TcYFbcQixZ7lVTiIk"
