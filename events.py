import discord
import re
import tweepy  # Assurez-vous que Tweepy est installé
from config import ROLE_TOUGEN_ANKI_ID, WELCOME_THREAD_ID, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET, TWITTER_TOUGEN_CHANNEL_ID
import asyncio

class TwitterStream(tweepy.StreamingClient):
    def __init__(self, bearer_token, bot):
        super().__init__(bearer_token)
        self.bot = bot

    def on_tweet(self, tweet):
        # Filtrer les retweets et les réponses
        if tweet.referenced_tweets or tweet.text.startswith("RT"):
            return

        # Construire le message à envoyer sur Discord
        tweet_url = f"https://twitter.com/{tweet.author_id}/status/{tweet.id}"
        message = f"📢 Nouveau tweet : {tweet_url}"

        # Envoyer le message sur le canal Discord
        asyncio.run_coroutine_threadsafe(
            self.send_to_discord(message), self.bot.loop
        )

    async def send_to_discord(self, message):
        channel = self.bot.get_channel(TWITTER_TOUGEN_CHANNEL_ID)
        if channel:
            await channel.send(message)

async def start_twitter_stream(bot):
    try:
        # Initialiser le flux Twitter
        stream = TwitterStream(bearer_token=TWITTER_API_KEY, bot=bot)
        stream.add_rules(tweepy.StreamRule("from:1260150204696686592"))  # Remplacez par l'ID du compte Twitter cible
        stream.filter()
    except Exception as e:
        print(f"Erreur lors du démarrage du flux Twitter : {str(e)}")

async def setup(bot):
    @bot.event
    async def on_ready():
        print(f'Bot connecté en tant que {bot.user.name}')
        await bot.change_presence(activity=discord.Game(name="Lire Tougen Anki"))
        from utils import start_webserver
        await start_webserver(bot)

        # Démarrer le flux Twitter
        asyncio.create_task(start_twitter_stream(bot))

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
            
    @bot.event
    async def on_message(message):
        try:
            # Vérifier si le message est dans le fil de bienvenue
            if message.channel.id == WELCOME_THREAD_ID:
                content_lower = message.content.lower()
                
                # Liste des modèles de questions à détecter
                question_patterns = [
                    # Questions sur le prochain chapitre
                    r"quand\s+(?:sort|sortira|est|sera)\s+(?:le\s+)?prochain\s+chapitre",
                    r"prochain\s+chapitre\s+(?:quand|date|sort|sortie)",
                    r"(?:date|jour)\s+(?:de|du|pour)\s+(?:la\s+)?(?:sortie|parution)\s+(?:du\s+)?(?:prochain\s+)?chapitre",
                    r"chapitre\s+(?:suivant|prochain)\s+(?:date|quand|prévu)",
                    # Questions plus générales
                    r"à\s+quelle\s+date\s+(?:le\s+)?(?:prochain|nouveau)\s+chapitre",
                    r"combien\s+(?:de\s+)?(?:temps|jours)\s+(?:avant|pour)\s+(?:le\s+)?(?:prochain|nouveau)\s+chapitre",
                    # Questions simples
                    r"prochain\s+chapitre\s*\?",
                    r"chapitre\s+quand\s*\?",
                ]
                
                # Vérifie si l'une des expressions régulières correspond
                should_respond = any(re.search(pattern, content_lower) for pattern in question_patterns)
                
                # Solution alternative simplifiée avec mots-clés (au cas où les regex échouent)
                keywords_combinations = [
                    ["quand", "prochain", "chapitre"],
                    ["date", "chapitre"],
                    ["sortie", "chapitre"],
                    ["prochain", "chapitre"],
                    ["chapitre", "suivant"],
                ]
                
                # Vérifie si tous les mots d'une combinaison sont présents
                for keywords in keywords_combinations:
                    if all(keyword in content_lower for keyword in keywords) and not should_respond:
                        should_respond = True
                        break
                    
                if should_respond:
                    # Réponse avec la date du prochain chapitre
                    response = discord.Embed(
                        title="📅 Date du prochain chapitre",
                        description="Le prochain chapitre de Tougen Anki sera disponible le **plus vite que possible**.",
                        color=0x0066FF
                    )
                    
                    response.add_field(
                        name="💫 Restez connectés",
                        value=f"Nous vous notifierons dès sa sortie avec le rôle <@&{ROLE_TOUGEN_ANKI_ID}>!",
                        inline=False
                    )
                    
                    # Ajouter des boutons pour d'autres questions fréquentes
                    view = discord.ui.View()
                    view.add_item(discord.ui.Button(
                        label="Tous les Chapitres", 
                        style=discord.ButtonStyle.secondary,
                        custom_id="previous_chapters"
                    ))
                    view.add_item(discord.ui.Button(
                        label="Où lire le manga ?", 
                        style=discord.ButtonStyle.secondary,
                        custom_id="where_to_read"
                    ))
                    
                    await message.reply(embed=response, view=view)
            
            # Traiter les commandes
            await bot.process_commands(message)
                
        except Exception as e:
            print(f"Erreur lors du traitement du message : {str(e)}")
            
    # Gestionnaire d'interactions pour les boutons
    @bot.event
    async def on_interaction(interaction):
        try:
            if interaction.type == discord.InteractionType.component:
                custom_id = interaction.data["custom_id"]
                
                if custom_id == "previous_chapters":
                    embed = discord.Embed(
                        title="📚 Tous les Chapitres",
                        description="Vous pouvez retrouver tous les chapitres sur notre [site](https://lanortrad.netlify.app/manga/tougen%20anki).",
                        color=0x0066FF
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
                elif custom_id == "where_to_read":
                    embed = discord.Embed(
                        title="📖 Où lire Tougen Anki ?",
                        description="Le manga est disponible en version française sur le [site](https://lanortrad.netlify.app/manga/tougen%20anki).",
                        color=0x0066FF
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
        except Exception as e:
            print(f"Erreur lors du traitement de l'interaction : {str(e)}")
