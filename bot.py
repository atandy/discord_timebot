import os
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = int(os.environ["GUILD_ID"])

REGIONS = [
    ("US-Hawaii",   "Pacific/Honolulu"),
    ("US-West",     "America/Los_Angeles"),
    ("US-Mountain", "America/Denver"),
    ("US-Central",  "America/Chicago"),
    ("US-East",     "America/New_York"),
    ("EU-France",   "Europe/Paris"),
    ("EU-Turkey",   "Europe/Istanbul"),
    ("Japan",       "Asia/Tokyo"),
]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.Object(id=GUILD_ID)


@tree.command(name="time", description="Show the current time across configured regions.", guild=guild)
async def time_command(interaction: discord.Interaction):
    now = datetime.now(ZoneInfo("UTC"))
    label_width = max(len(label) for label, _ in REGIONS)
    lines = []
    for label, tz in REGIONS:
        local = now.astimezone(ZoneInfo(tz))
        lines.append(
            f"{label:<{label_width}}  {local:%Y-%m-%d}  {local:%H:%M} ({local:%I:%M %p})  {local:%Z}"
        )
    body = "\n".join(lines)
    await interaction.response.send_message(
        f"Here are the current local times in the following regions:\n```\n{body}\n```"
    )


@client.event
async def on_ready():
    await tree.sync(guild=guild)
    print(f"Logged in as {client.user} — slash commands synced to guild {GUILD_ID}")


if __name__ == "__main__":
    client.run(TOKEN)
