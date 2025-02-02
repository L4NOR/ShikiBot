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

# Supprimer la commande help par défaut
bot.remove_command('help')

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
    # ID du fil pour les messages
    thread_id = 1330144191816142941
    
    try:
        # Obtenir le fil (thread)
        thread = await bot.fetch_channel(thread_id)
        if not thread:
            print(f"Fil {thread_id} non trouvé")
            return
        
        # Vérifier si le rôle a été ajouté
        role = after.guild.get_role(role_id)
        if not role:
            print(f"Rôle {role_id} non trouvé")
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

# Commande Shiki (aide)
@bot.command(name='Shiki')
async def help_command(ctx):
    embed = discord.Embed(
        title="🔥 Guide du Bot Tougen Anki 🔥",
        description=(
            "Bienvenue dans l'univers de Tougen Anki ! \n"
            "🤖 Votre assistant de communauté dédié aux fans du manga"
        ),
        color=0xFF1493  # Bleu exorciste
    )

    # Commandes administrateur avec icônes et formatage amélioré
    embed.add_field(
        name="👑 Commandes Administrateur",
        value=(
            "!newchapter_tougenanki\n"
            "• 📘 Annonce un nouveau chapitre\n"
            "• 🔢 Paramètres : <numéro> <lien> [description]\n"
            "• 💡 Exemple : !newchapter_tougenanki 1 https://exemple.com"
        ),
        inline=False
    )

    # Section informative avec plus de détails
    embed.add_field(
        name="🌟 Fonctionnalités du Bot",
        value=(
            "• 👋 Gestion des messages de bienvenue dans l'univers de Tougen Anki\n"
            "• 📣 Notifications de nouveaux chapitres\n"
            "• 🏷️ Suivi automatique des rôles\n"
            "• 🔔 Alertes communautaires"
        ),
        inline=False
    )

    # Nouveaux détails interactifs
    embed.add_field(
        name="🎉 Interaction Communautaire",
        value=(
            "• Réactions automatiques aux annonces\n"
            "• Création de threads de discussion\n"
            "• Mentions de rôles personnalisées"
        ),
        inline=False
    )

    embed.set_footer(
        text="Un problème ? Contactez les administrateurs | Powered by Tougen Anki Bot 🍑👹",
        icon_url=""  # Remplacez par une URL d'icône valide
    )

    await ctx.send(embed=embed)

# Commande pour annoncer un nouveau chapitre
@bot.command(name='newchapter_tougenanki')
@commands.has_permissions(administrator=True)
async def announce_new_chapter(ctx, chapter_number: str, chapter_link: str, *, description: str = None):
    if ctx.channel.id != 1326213946188890142:
        await ctx.send("Cette commande ne peut être utilisée que dans le canal d'annonces approprié.")
        return

    role_id = 1326778962143215677
    role = ctx.guild.get_role(role_id)
    
    if not role:
        await ctx.send("Le rôle spécifié n'a pas été trouvé.")
        return

    # Créer l'embed avec un design amélioré
    embed = discord.Embed(
        title="🔥 NOUVEAU CHAPITRE DE TOUGEN ANKI 🔥",
        description=(
            "Un nouveau chapitre vient d'arriver ! Préparez-vous à plonger dans de nouvelles "
            "aventures palpitantes avec Shiki Ichinose et son envie d'un monde de paix entre Momo et Oni !\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=0x1E90FF  # Bleu royal
    )
    
    # Informations sur le chapitre
    embed.add_field(
        name="📖 Chapitre",
        value=f"**#{chapter_number}**",
        inline=True
    )
    
    embed.add_field(
        name="⏰ Disponible",
        value="**MAINTENANT !**",
        inline=True
    )
    
    # Lien de lecture
    embed.add_field(
        name="📚 Lien de lecture",
        value=f"[Cliquez ici pour lire le chapitre !]({chapter_link})",
        inline=False
    )
    
    # Séparateur
    embed.add_field(
        name="━━━━━━━━━━━━━━━━━━━━━━━━",
        value="",
        inline=False
    )
    
    # Description si fournie
    if description:
        embed.add_field(
            name="📝 Aperçu",
            value=f"*{description}*",
            inline=False
        )
    
    # Note de bas de page
    embed.set_footer(
        text=(
            "N'oubliez pas de partager vos théories et réactions sur twitter et discord ! "
            "Bonne lecture à tous ! 🎉"
        )
    )
    
    # Petit rappel en haut du message
    reminder_text = (
        f"{role.mention}\n"
        "───────────────────────\n"
        "**Un nouveau chapitre vient d'être publié !**\n"
        "Retrouvez tous les détails ci-dessous ⬇️"
    )

    # Envoyer l'annonce
    announcement = await ctx.send(reminder_text, embed=embed)
    
    # Ajouter plusieurs réactions
    reactions = ["🔥", "👀", "❤️"]
    for reaction in reactions:
        await announcement.add_reaction(reaction)

    # Créer un thread pour la discussion dans la catégorie spécifiée
    category = ctx.guild.get_channel(1326230010608226364)
    if category:
        thread = await announcement.create_thread(
            name=f"Tougen Anki - Discussion Chapitre {chapter_number}",
            auto_archive_duration=1440  # Archive après 24h d'inactivité
    )
    
    # Supprimer la commande originale
    await ctx.message.delete()

# Lancer le bot avec asyncio
async def main():
    async with bot:
        await bot.start(os.getenv('TOKEN'))

# Point d'entrée principal
if __name__ == "__main__":
    asyncio.run(main())
