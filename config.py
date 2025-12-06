import os
from dotenv import load_dotenv
import discord

# Charger les variables d'environnement
load_dotenv()

# Configuration du bot
BOT_TOKEN = os.getenv('TOKEN')
PORT = int(os.getenv('PORT', 8080))
COMMAND_PREFIX = 's!'

# ID des rôles et canaux
ROLE_TOUGEN_ANKI_ID = 1326778962143215677
WELCOME_THREAD_ID = 1330144191816142941
ANNOUNCEMENTS_CHANNEL_ID = 1326213946188890142
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

# IDs des rôles de l'équipe de traduction (à remplacer par les vrais IDs)
ROLE_TRADUCTEUR_ID = 433305136975183882  
ROLE_CLEANER_ID = 608234789564186644
ROLE_EDITEUR_ID = 608234789564186644
ROLE_QCHECK_ID = 937386825562062858

# Cooldown pour les commandes d'incitation (en secondes)
INCITATION_COOLDOWN = 300  # 5 minutes entre chaque incitation du même type

# Configuration du timer
TIMER_UPDATE_INTERVAL = 60 * 60  # Mise à jour toutes les heures
TIMER_STATUS_COLORS = {
    'EARLY': 0x00FF00,    # Vert
    'SOON': 0xFFFF00,     # Jaune
    'IMMINENT': 0xFF0000  # Rouge
}