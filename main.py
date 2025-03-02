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
            "• 🔢 Paramètres : <numéros_chapitres> <lien> [description]\n"
            "• 💡 Exemple : !newchapter_tougenanki 187 188 https://exemple.com"
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

# Commande pour annoncer un nouveau chapitre (modifiée pour accepter plusieurs chapitres)
@bot.command(name='newchapter_tougenanki')
@commands.has_permissions(administrator=True)
async def announce_new_chapter(ctx, *args):
    if ctx.channel.id != 1326213946188890142:
        await ctx.send("Cette commande ne peut être utilisée que dans le canal d'annonces approprié.")
        return
    
    # Vérifier qu'il y a au moins 2 arguments (au moins un numéro de chapitre et un lien)
    if len(args) < 2:
        await ctx.send("Syntaxe incorrecte. Utilisez `!newchapter_tougenanki <numéros_chapitres> <lien> [description]`")
        return
    
    # Trouver où se termine la liste des chapitres et où commence le lien
    chapter_numbers = []
    link_index = 0
    
    for i, arg in enumerate(args):
        # Si l'argument ressemble à un URL (commence par http), c'est notre lien
        if arg.startswith("http"):
            link_index = i
            break
        # Sinon, c'est un numéro de chapitre
        chapter_numbers.append(arg)
    
    # Si aucun lien n'a été trouvé
    if link_index == 0:
        await ctx.send("Lien manquant. Utilisez `!newchapter_tougenanki <numéros_chapitres> <lien> [description]`")
        return
    
    chapter_link = args[link_index]
    
    # Récupérer la description si elle existe (tout ce qui vient après le lien)
    description = None
    if link_index + 1 < len(args):
        description = " ".join(args[link_index + 1:])
    
    # Formater les numéros de chapitres pour l'affichage
    chapters_display = ", ".join(chapter_numbers)
    
    role_id = 1326778962143215677
    role = ctx.guild.get_role(role_id)
    
    if not role:
        await ctx.send("Le rôle spécifié n'a pas été trouvé.")
        return

    # Créer l'embed avec un design amélioré
    embed = discord.Embed(
        title="🔥 NOUVEAU(X) CHAPITRE(S) DE TOUGEN ANKI 🔥",
        description=(
            "De nouveaux chapitres viennent d'arriver ! Préparez-vous à plonger dans de nouvelles "
            "aventures palpitantes avec Shiki Ichinose et son envie d'un monde de paix entre Momo et Oni !\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=0x1E90FF  # Bleu royal
    )
    
    # Informations sur le chapitre
    embed.add_field(
        name="📖 Chapitre(s)",
        value=f"**#{chapters_display}**",
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
        value=f"[Cliquez ici pour lire le(s) chapitre(s) !]({chapter_link})",
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
        "**De nouveaux chapitres viennent d'être publiés !**\n"
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
        thread_name = f"Tougen Anki - Discussion Chapitre(s) {chapters_display}"
        thread = await announcement.create_thread(
            name=thread_name,
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
