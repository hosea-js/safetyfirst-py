import discord
import dotenv
import os
import json
from datetime import datetime, timezone
from services import bmkg_servc

dotenv.load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="ping", description="Ping, Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Command will be developed later after caching system working and ready.
# @tree.command(name="status", description="Check the status for API that used, Discord Gateaway status, and other information.")
# async def status(interaction: discord.interaction):
#    await 

@tree.command(name="quake", description="Get the latest earthquake")
async def quake(interaction: discord.Interaction):
    data = await bmkg_servc.get_latest_quake()
    gempa = data["Infogempa"]["gempa"]
    embed = build_quake_embed(gempa)
    await interaction.response.send_message(embed=embed)

def build_quake_embed(gempa: dict) -> discord.Embed:
    magnitude = float(gempa["Magnitude"])
    coordinate = gempa["Coordinates"]
    dt = datetime.fromisoformat(gempa["DateTime"])
    utc_text = dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lcltime = discord.utils.format_dt(dt, style="F") 
    embed = discord.Embed(
        title="🌎 Latest Earthquake",
        color=discord.Colour(0x1E88E5),
    )
    embed.add_field(name="Magnitude", value=f"{magnitude} M", inline=True)
    embed.add_field(name="Depth", value=gempa["Kedalaman"], inline=True)
    embed.add_field(name="Location", value=f"Google Maps: https://maps.google.com/?q={coordinate}", inline=False)
    embed.add_field(name="Coordinates", value=gempa["Coordinates"], inline=False)
    embed.add_field(name="Time (UTC)", value=utc_text, inline=True)
    embed.add_field(name="Time (Local)", value=lcltime, inline=True)
    embed.set_image(url=f"https://static.bmkg.go.id/{gempa['Shakemap']}")
    embed.set_footer(text="Source: Badan Meteorologi, Klimatologi, dan Geofisika Indonesia")
    return embed

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user.name} - {client.user.id}')
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')    

@client.event
async def on_member_join(member):
    channel = member.guild.get_channel(1568481899956146196)
    await channel.send(f"Welcome, {member.mention}!")


client.run(os.getenv('BOT_TOKEN'))