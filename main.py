import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer
import os

SERVER_IP = "mc.angelup.eu"
SERVER_PORT = 27727

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash příkazy synchronizovány: {len(synced)}")
    except Exception as e:
        print(f"Chyba při synchronizaci: {e}")

@bot.tree.command(name="start", description="Spustí Minecraft server (nebo oznámí spuštění)")
async def start_command(interaction: discord.Interaction):
    await interaction.response.send_message("🟢 Spouštím Minecraft server...")

@bot.tree.command(name="status", description="Zobrazí stav Minecraft serveru")
async def status_command(interaction: discord.Interaction):
    try:
        server = JavaServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")
        status = server.status()
        await interaction.response.send_message(
            f"✅ Server je online!\nHráči: {status.players.online}/{status.players.max}"
        )
    except Exception:
        await interaction.response.send_message("🔴 Server je offline nebo nedostupný.")

bot.run(os.getenv("DISCORD_TOKEN"))
