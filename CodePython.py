import discord 
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import nest_asyncio
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Le token doit être défini dans le fichier .env

# Connexion à Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("clebottest.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1yOJ-WJdRXEKoN5uetyN5wy2bEYRH6jY6GJLQtUgSzJE").sheet1

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot started successfully!")

@bot.command()
async def prix(ctx, *, nom_annee: str):
    print(f"{nom_annee} demandé")
    data = sheet.get_all_records()
    for ligne in data:
        if ligne["Annee"].lower() == nom_annee.lower():
            await ctx.send(f"{ligne['Annee']} coûte {ligne['Prix']}€")
            return
    await ctx.send("pas cet annee")

@bot.event

async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()

    if content.startswith("!"):
        try:
            commande = content[1:].strip()
            elements = commande.split()

            if len(elements) == 3 and elements[0].isdigit() and len(elements[0]) == 4:
                annee, classe, type_ = elements
                data = sheet.get_all_records()

                for ligne in data:
                    if (
                        str(ligne["Annee"]).strip() == annee and
                        ligne["Classe"].strip().upper() == classe.upper() and
                        ligne["Type"].strip().upper() == type_.upper()
                    ):
                        sujet = ligne.get("URL sujet", "").strip()
                        corrige = ligne.get("URL corrige", "").strip()
                        Notice = ligne.get("URL rapport", "").strip()

                        # On vérifie si chaque lien commence bien par http
                        lien_sujet = sujet if sujet.lower().startswith("http") else "non disponible"
                        lien_corrige = corrige if corrige.lower().startswith("http") else "non disponible"
                        lien_Notice = Notice.strip()
                        lien_Notice = lien_Notice if "http" in lien_Notice else "non disponible"


                        reponse = (
                            f"**{annee} {classe.upper()} {type_.upper()}**\n"
                            f"📘 Sujet : {lien_sujet}\n"
                            f"🛠️ Corrigé : {lien_corrige}\n"
                            f"📄 Notice : {lien_Notice}"
                        )

                        await message.channel.send(reponse)
                        return

                await message.channel.send("❌ Aucune correspondance trouvée dans la feuille.")
                return
            else:
                await message.channel.send("❌ Erreur de format. Utilise : `!2023 CCS M1` ou `!2018 CCS P2`")
                return

        except Exception as e:
            await message.channel.send(f"⚠️ Erreur inattendue : {str(e)}")
            return

    await bot.process_commands(message)

nest_asyncio.apply()

async def main():
    await bot.start(DISCORD_TOKEN)

asyncio.run(main())



