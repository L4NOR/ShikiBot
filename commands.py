import discord
from discord.ext import commands
import random
from config import PINK_COLOR, ROYAL_BLUE_COLOR, ROLE_TOUGEN_ANKI_ID, ANNOUNCEMENTS_CHANNEL_ID, ANNOUNCEMENT_REACTIONS
from config import DISCUSSIONS_CATEGORY_ID, THREAD_AUTO_ARCHIVE_DURATION
from config import ROLE_TRADUCTEUR_ID, ROLE_CLEANER_ID, ROLE_EDITEUR_ID, ROLE_QCHECK_ID, INCITATION_COOLDOWN

# ID du canal de test
TEST_CHANNEL_ID = 1330221808753840159

# Messages d'incitation amusants pour chaque rôle
INCITATION_MESSAGES = {
    'trad': [
        "📝 Les traducteurs ! Les lecteurs s'impatientent ! Leurs yeux scrutent l'horizon en quête de nouveaux chapitres ! 👀",
        "🔥 Ô grands maîtres de la traduction ! Vos fidèles lecteurs attendent avec ferveur vos précieuses lignes !",
        "⚡ ALERTE ! Les fans de Tougen Anki sont en manque ! Traducteurs, à vos claviers !",
        "🍵 Petit thé et traduction ? Les lecteurs vous envoient leur énergie ! ✨",
        "📚 Les pages blanches pleurent... Elles ont besoin de vos traductions pour vivre !",
        "🎭 Shiki lui-même vous encourage à traduire plus vite ! (enfin, on suppose...)",
        "💪 Courage les traducteurs ! Chaque mot traduit est un pas vers la paix entre Momo et Oni !",
    ],
    'clean': [
        "🧹 Cleaners ! Les bulles ont besoin de vous ! Faites briller ces pages !",
        "✨ Les pages attendent leur cure de beauté ! Cleaners, à l'action !",
        "🎨 Sans vous, les pages seraient tristes... Cleaners, illuminez-les !",
        "🧼 NETTOYAGE EN COURS... ou pas ? Les lecteurs comptent sur vous !",
        "💎 Polissez ces pages comme des diamants ! Les fans n'attendent que ça !",
        "🌟 Les cleaners sont les héros silencieux ! Montrez votre pouvoir !",
        "🔮 Faites disparaître ces textes japonais comme par magie !",
    ],
    'edit': [
        "✏️ Éditeurs ! L'heure est venue de placer ces textes avec art !",
        "🎯 Les bulles vides vous appellent ! Éditeurs, remplissez-les !",
        "📐 Précision et style ! Les éditeurs sont la clé du succès !",
        "💫 Sans édition, pas de lecture ! Les fans comptent sur votre talent !",
        "🖊️ Les polices de caractères s'ennuient... Éditeurs, donnez-leur vie !",
        "🎪 Place aux artistes de l'édition ! Le spectacle doit continuer !",
        "📱 Les lecteurs rafraîchissent frénétiquement... Éditeurs, à vous de jouer !",
    ],
    'qcheck': [
        "🔍 Quality Checkers ! Les coquilles tremblent devant vous ! Traquez-les !",
        "🛡️ Gardiens de la qualité ! Les lecteurs comptent sur votre œil de lynx !",
        "⚖️ La perfection n'attend pas ! QCheckers, à vos marques !",
        "🎖️ Dernière ligne de défense ! Les QCheckers sont notre espoir !",
        "🔬 Analysez, vérifiez, validez ! La qualité avant tout !",
        "👁️ Rien n'échappe aux QCheckers ! Prouvez-le encore une fois !",
        "✅ Le tampon de validation attend ! QCheckers, c'est l'heure !",
    ],
}

# Couleurs pour chaque type d'incitation
INCITATION_COLORS = {
    'trad': 0x3498DB,     # Bleu
    'clean': 0x2ECC71,    # Vert
    'edit': 0xE74C3C,     # Rouge
    'qcheck': 0x9B59B6,   # Violet
}

# Emojis pour chaque type
INCITATION_EMOJIS = {
    'trad': "📝",
    'clean': "🧹",
    'edit': "✏️",
    'qcheck': "🔍",
}

# Titres pour chaque type
INCITATION_TITLES = {
    'trad': "Incitation à la Traduction !",
    'clean': "Incitation au Cleaning !",
    'edit': "Incitation à l'Édition !",
    'qcheck': "Incitation au Quality Check !",
}

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

        # Section des commandes d'incitation
        embed.add_field(
            name="📢 Commandes d'Incitation",
            value=(
                "• `s!trad` - Encourager les traducteurs\n"
                "• `s!clean` - Encourager les cleaners\n"
                "• `s!edit` - Encourager les éditeurs\n"
                "• `s!qcheck` - Encourager les quality checkers\n"
                "• `s!team` - Encourager toute l'équipe !"
            ),
            inline=False
        )

        embed.set_footer(
            text="Un problème ? Contactez les administrateurs | Powered by Tougen Anki Bot 💀👹",
        )

        await ctx.send(embed=embed)

    # Fonction générique pour créer une commande d'incitation
    async def send_incitation(ctx, incitation_type: str, role_id: int):
        """Envoie un message d'incitation pour un rôle spécifique."""
        
        # Récupérer le rôle
        role = ctx.guild.get_role(role_id)
        
        # Choisir un message aléatoire
        message = random.choice(INCITATION_MESSAGES[incitation_type])
        
        # Créer l'embed
        embed = discord.Embed(
            title=f"{INCITATION_EMOJIS[incitation_type]} {INCITATION_TITLES[incitation_type]}",
            description=message,
            color=INCITATION_COLORS[incitation_type]
        )
        
        # Ajouter des informations sur qui a lancé l'incitation
        embed.add_field(
            name="🙋 Demandé par",
            value=f"{ctx.author.mention}",
            inline=True
        )
        
        # Ajouter un compteur de demandes (optionnel - pour le fun)
        embed.add_field(
            name="💭 Message",
            value="Les lecteurs ont hâte de lire la suite !",
            inline=True
        )
        
        embed.set_footer(
            text="Utilisez les commandes d'incitation avec modération ! 😊",
        )
        
        # Mentionner le rôle si l'ID est valide (non nul)
        if role and role_id != 0:
            await ctx.send(f"{role.mention}", embed=embed)
        else:
            await ctx.send(embed=embed)
        
        # Ajouter des réactions
        # Note: On ne peut pas ajouter de réactions à un message sans le récupérer d'abord

    # Commande d'incitation pour les traducteurs
    @bot.command(name='trad')
    @commands.cooldown(1, INCITATION_COOLDOWN, commands.BucketType.guild)
    async def incite_trad(ctx):
        """Encourage les traducteurs à avancer sur le chapitre."""
        await send_incitation(ctx, 'trad', ROLE_TRADUCTEUR_ID)

    # Commande d'incitation pour les cleaners
    @bot.command(name='clean')
    @commands.cooldown(1, INCITATION_COOLDOWN, commands.BucketType.guild)
    async def incite_clean(ctx):
        """Encourage les cleaners à avancer sur le chapitre."""
        await send_incitation(ctx, 'clean', ROLE_CLEANER_ID)

    # Commande d'incitation pour les éditeurs
    @bot.command(name='edit')
    @commands.cooldown(1, INCITATION_COOLDOWN, commands.BucketType.guild)
    async def incite_edit(ctx):
        """Encourage les éditeurs à avancer sur le chapitre."""
        await send_incitation(ctx, 'edit', ROLE_EDITEUR_ID)

    # Commande d'incitation pour les quality checkers
    @bot.command(name='qcheck')
    @commands.cooldown(1, INCITATION_COOLDOWN, commands.BucketType.guild)
    async def incite_qcheck(ctx):
        """Encourage les quality checkers à valider le chapitre."""
        await send_incitation(ctx, 'qcheck', ROLE_QCHECK_ID)

    # Commande pour inciter toute l'équipe
    @bot.command(name='team')
    @commands.cooldown(1, INCITATION_COOLDOWN * 2, commands.BucketType.guild)
    async def incite_team(ctx):
        """Encourage toute l'équipe de traduction !"""
        
        # Messages pour toute l'équipe
        team_messages = [
            "🚀 ÉQUIPE DE TRADUCTION ! Les lecteurs croient en vous ! Ensemble, vous êtes imbattables !",
            "⭐ Du traducteur au QChecker, vous formez une équipe de légende ! Les fans vous adorent !",
            "🎊 Toute l'équipe est sollicitée ! Les lecteurs envoient leur énergie positive !",
            "💖 Traducteurs, Cleaners, Éditeurs, QCheckers... Vous êtes les héros de la communauté !",
            "🌈 L'équipe au complet ! Rien ne peut vous arrêter ! Les chapitres n'attendent que vous !",
            "🔥 MOBILISATION GÉNÉRALE ! L'équipe de traduction doit montrer sa puissance !",
        ]
        
        embed = discord.Embed(
            title="🌟 Incitation Générale - Toute l'Équipe ! 🌟",
            description=random.choice(team_messages),
            color=0xFFD700  # Or
        )
        
        embed.add_field(
            name="📝 Traduction",
            value="Les mots attendent !",
            inline=True
        )
        
        embed.add_field(
            name="🧹 Cleaning",
            value="Les pages brillent !",
            inline=True
        )
        
        embed.add_field(
            name="✏️ Édition",
            value="Les bulles appellent !",
            inline=True
        )
        
        embed.add_field(
            name="🔍 QCheck",
            value="La qualité prime !",
            inline=True
        )
        
        embed.add_field(
            name="🙋 Demandé par",
            value=f"{ctx.author.mention}",
            inline=False
        )
        
        embed.set_footer(
            text="L'union fait la force ! 💪 | Powered by Tougen Anki Bot",
        )
        
        # Mentionner tous les rôles si disponibles
        mentions = []
        for role_id in [ROLE_TRADUCTEUR_ID, ROLE_CLEANER_ID, ROLE_EDITEUR_ID, ROLE_QCHECK_ID]:
            if role_id != 0:
                role = ctx.guild.get_role(role_id)
                if role:
                    mentions.append(role.mention)
        
        if mentions:
            await ctx.send(" ".join(mentions), embed=embed)
        else:
            await ctx.send(embed=embed)

    # Gestion des erreurs de cooldown pour les commandes d'incitation
    @incite_trad.error
    @incite_clean.error
    @incite_edit.error
    @incite_qcheck.error
    async def incitation_cooldown_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = int(error.retry_after // 60)
            seconds = int(error.retry_after % 60)
            await ctx.send(
                f"⏳ Doucement ! Cette commande est en cooldown. "
                f"Réessayez dans **{minutes}m {seconds}s**. "
                f"On ne veut pas spammer l'équipe ! 😅"
            )
        else:
            await ctx.send(f"Une erreur s'est produite: {str(error)}")

    @incite_team.error
    async def team_cooldown_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = int(error.retry_after // 60)
            seconds = int(error.retry_after % 60)
            await ctx.send(
                f"⏳ La commande team a un cooldown plus long ! "
                f"Réessayez dans **{minutes}m {seconds}s**. "
                f"Patience, jeune fan ! 🙏"
            )
        else:
            await ctx.send(f"Une erreur s'est produite: {str(error)}")

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
                "━━━━━━━━━━━━━━━━━━━━━━━"
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
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="",
            inline=False
        )
        
        # Description si fournie
        if description:
            embed.add_field(
                name="🔍 Aperçu",
                value=f"{description}",
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

    # Commande TEST pour annoncer un nouveau chapitre
    @bot.command(name='test_newchapter_tougenanki')
    @commands.has_permissions(administrator=True)
    async def test_announce_new_chapter(ctx, *args):
        if ctx.channel.id != TEST_CHANNEL_ID:
            await ctx.send("Cette commande ne peut être utilisée que dans le canal de test.")
            return
        
        # Vérifier qu'il y a au moins 2 arguments (au moins un numéro de chapitre et un lien)
        if len(args) < 2:
            await ctx.send("Syntaxe incorrecte. Utilisez `!test_newchapter_tougenanki <numéros_chapitres> <lien> [description]`")
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
            await ctx.send("Lien manquant. Utilisez `!test_newchapter_tougenanki <numéros_chapitres> <lien> [description]`")
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
            title="🔥 [TEST] NOUVEAU(X) CHAPITRE(S) DE TOUGEN ANKI 🔥",
            description=(
                "**⚠️ CECI EST UN TEST ⚠️**\n\n"
                "De nouveaux chapitres viennent d'arriver ! Préparez-vous à plonger dans de nouvelles "
                "aventures palpitantes avec Shiki Ichinose et son envie d'un monde de paix entre Momo et Oni !\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━"
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
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="",
            inline=False
        )
        
        # Description si fournie
        if description:
            embed.add_field(
                name="🔍 Aperçu",
                value=f"{description}",
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
            "**[TEST] De nouveaux chapitres viennent d'être publiés !**\n"
            "Retrouvez tous les détails ci-dessous ⬇️"
        )

        # Envoyer l'annonce
        announcement = await ctx.send(reminder_text, embed=embed)
        
        # Ajouter plusieurs réactions
        for reaction in ANNOUNCEMENT_REACTIONS:
            await announcement.add_reaction(reaction)
        
        # Supprimer la commande originale
        await ctx.message.delete()

    # Gestion des erreurs pour la commande newchapter_tougenanki
    @announce_new_chapter.error
    async def announce_new_chapter_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Il manque des arguments. Usage: !newchapter_tougenanki <numéros_chapitres> <lien> [description]")
        else:
            await ctx.send(f"Une erreur s'est produite: {str(error)}")

    # Gestion des erreurs pour la commande test
    @test_announce_new_chapter.error
    async def test_announce_new_chapter_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Il manque des arguments. Usage: !test_newchapter_tougenanki <numéros_chapitres> <lien> [description]")
        else:
            await ctx.send(f"Une erreur s'est produite: {str(error)}")

    # Commande pour donner une récapitulation du dernier chapitre
    @bot.command(name='recap')
    async def recap_command(ctx):
        # Informations sur le dernier chapitre
        last_chapter_number = "193"  # Numéro du chapitre
        last_chapter_title = "Sentiments"  # Titre du chapitre
        last_chapter_summary = (
            "Yusurube perd le contrôle et entre en mode berserk après avoir réalisé que sa sœur est réellement morte, brisant l'illusion créée par un lavage de cerveau. Alors qu'il sombre dans la douleur, ses amis tentent de le ramener à la raison en lui rappelant qu'il n'est pas seul et qu'ils sont là pour le soutenir."
        )  # Résumé du chapitre
        chapter_link = "https://lanortrad.netlify.app/manga/tougen%20anki/chapitre%20193"  # Lien vers le chapitre

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
        )

        # Envoyer l'embed
        await ctx.send(embed=embed)