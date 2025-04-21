import discord
import os
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

# Carica il token da .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents richiesti
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

# Inizializza il bot
client = commands.Bot(command_prefix='!', intents=intents)

# ID dei canali
LOG_CHANNEL_ID = 1363882148469280968
VOICE_CHANNEL_ID = 1357046135981740263

# Registro entrate/uscite
timbrature = {}

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

@client.event
async def on_ready():
    print(f'✅ Bot connesso come {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == VOICE_CHANNEL_ID and (before.channel != after.channel):
        ora = get_timestamp()
        timbrature[member.id] = ora
        log = f"🟢 ENTRATA | {member.name} | {ora}"
        print(log)
        await send_log(log)
    elif before.channel and before.channel.id == VOICE_CHANNEL_ID and (after.channel != before.channel):
        ora = get_timestamp()
        entrata = timbrature.pop(member.id, 'N/D')
        log = f"🔴 USCITA  | {member.name} | {ora} (Entrata: {entrata})"
        print(log)
        await send_log(log)

async def send_log(messaggio):
    canale = client.get_channel(LOG_CHANNEL_ID)
    if canale:
        await canale.send(messaggio)

# Avvia il bot
client.run(TOKEN)
