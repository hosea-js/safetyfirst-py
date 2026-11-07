import discord
import dotenv
import os

dotenv.load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="ping", description="Ping, Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

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