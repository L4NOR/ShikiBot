import discord
from discord.ext import commands
from config import PINK_COLOR, ROYAL_BLUE_COLOR, ROLE_TOUGEN_ANKI_ID, ANNOUNCEMENTS_CHANNEL_ID, ANNOUNCEMENT_REACTIONS
from config import DISCUSSIONS_CATEGORY_ID, THREAD_AUTO_ARCHIVE_DURATION
from datetime import datetime
import re
from config import WELCOME_THREAD_ID

def setup_commands(bot):
    # Commande Shiki (aide)
    @bot.command(name='Shiki')
    async def help_command(ctx):
        embed = discord.Embed(
            title="🔥 Guide du Bot Tougen Anki 🔥",
            description=(
                "Bienvenue dans l'univers de Tougen Anki ! \n"
                "🤖 Votre assistant de communauté dédié aux fans du manga"
            ),
            color=PINK_COLOR
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
    async def announce_new_chapter(ctx, *args):
        if ctx.channel.id != ANNOUNCEMENTS_CHANNEL_ID:
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
        
        role_id = ROLE_TOUGEN_ANKI_ID
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
            color=ROYAL_BLUE_COLOR
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
        for reaction in ANNOUNCEMENT_REACTIONS:
            await announcement.add_reaction(reaction)
        
        # Supprimer la commande originale
        await ctx.message.delete()

    # Commande pour donner une récapitulation du dernier chapitre
    @bot.command(name='recap')
    async def recap_command(ctx):
        # Informations sur le dernier chapitre
        last_chapter_number = "189"  # Numéro du chapitre
        last_chapter_title = "Pile de cadavres"  # Titre du chapitre
        last_chapter_summary = (
            "La grande bataille commence entre les Momo et les Oni. "
            "Pour gagner, Shiki et ses alliés doivent découvrir les secrets cachés derrière les artefacts ancestraux. "
            "Cependant, une trahison inattendue pourrait tout bouleverser..."
        )  # Résumé du chapitre
        chapter_link = "https://lanortrad.netlify.app/manga/tougen%20anki/chapitre%20189"  # Lien vers le chapitre

        # Création de l'embed
        embed = discord.Embed(
            title=f"📖 Récapitulatif du Chapitre #{last_chapter_number}",
            description=f"**{last_chapter_title}**",
            color=PINK_COLOR
        )

        # Ajouter le résumé
        embed.add_field(
            name="Résumé",
            value=last_chapter_summary,
            inline=False
        )

        # Ajouter le lien vers le chapitre
        embed.add_field(
            name="📚 Lien vers le chapitre",
            value=f"[Cliquez ici pour lire le chapitre]({chapter_link})",
            inline=False
        )

        # Ajouter une note de bas de page
        embed.set_footer(
            text="Restez connectés pour le prochain chapitre !",
            icon_url=""  # Ajoutez une URL d'icône si nécessaire
        )

        # Envoyer l'embed
        await ctx.send(embed=embed)

    @bot.event
    async def on_message(message):
        # Vérifier si le message est dans le bon channel
        if message.channel.id != WELCOME_THREAD_ID:
            return

        # Ignorer les messages du bot lui-même
        if message.author.bot and message.author.name != "LanorTrad":
            return

        # Vérifier si c'est une commande de planification de LanorTrad
        if message.author.name == "LanorTrad":
            pattern = r'!planifier "Tougen Anki" (\d+) (\d{2}/\d{2}/\d{4})'
            match = re.search(pattern, message.content)
            
            if match:
                chapter_number = match.group(1)
                release_date = match.group(2)
                
                try:
                    # Convertir la date (format: DD/MM/YYYY)
                    release_datetime = datetime.strptime(release_date, "%d/%m/%Y")
                    
                    # Sauvegarder les informations
                    bot.next_chapter = {
                        'number': chapter_number,
                        'release_date': release_datetime,
                        'channel_id': WELCOME_THREAD_ID  # Sauvegarder l'ID du channel
                    }
                    
                    # Créer l'embed de confirmation
                    embed = create_timer_embed(chapter_number, release_datetime)
                    await message.channel.send(embed=embed)
                    
                except ValueError as e:
                    print(f"Erreur lors du traitement de la date : {e}")

        # Traiter les commandes normales du bot
        await bot.process_commands(message)

    @bot.command(name='timer')
    async def show_timer(ctx):
        """Affiche le timer pour le prochain chapitre"""
        # Vérifier si la commande est utilisée dans le bon channel
        if ctx.channel.id != WELCOME_THREAD_ID:
            await ctx.message.delete()
            return
            
        if not hasattr(bot, 'next_chapter'):
            await ctx.send("❌ Aucun chapitre n'est actuellement planifié.")
            return
            
        chapter_info = bot.next_chapter
        embed = create_timer_embed(chapter_info['number'], chapter_info['release_date'])
        await ctx.send(embed=embed)

def create_timer_embed(chapter_number, release_datetime):
    """Crée l'embed du timer avec les informations données"""
    now = datetime.now()
    delta = release_datetime - now
    
    embed = discord.Embed(
        title="⏰ Compte à rebours Tougen Anki",
        description=f"En attente du chapitre #{chapter_number}",
        color=ROYAL_BLUE_COLOR
    )
    
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    # Champs temporels
    embed.add_field(
        name="⌛ Temps restant",
        value=f"**{days}** jours, **{hours}** heures et **{minutes}** minutes",
        inline=False
    )
    
    # Date de sortie
    embed.add_field(
        name="📅 Date de sortie",
        value=release_datetime.strftime("%d/%m/%Y"),
        inline=True
    )
    
    # Barre de progression
    progress = min(100, int((1 - delta.total_seconds() / (7 * 24 * 3600)) * 100))
    progress_bar = "█" * (progress // 10) + "░" * ((100 - progress) // 10)
    
    embed.add_field(
        name="📊 Progression",
        value=f"`{progress_bar}` {progress}%",
        inline=False
    )
    
    # Status dynamique
    if days > 5:
        status = "🟢 Prenez votre temps pour relire les anciens chapitres !"
    elif days > 2:
        status = "🟡 Préparez-vous, le prochain chapitre arrive bientôt !"
    else:
        status = "🔴 Le chapitre est imminent ! Restez à l'affût !"
        
    embed.add_field(
        name="📌 Status",
        value=status,
        inline=False
    )
    
    embed.set_footer(
        text="Utilisez !timer pour voir le temps restant",
        icon_url=""
    )
    
    return embed
