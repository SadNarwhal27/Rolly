import os
import discord
from dotenv import load_dotenv
from enum import Enum
from rolling_dice import embed_maker, roll_character

class bot_client(discord.Client):
    """Creates the Discord client with intents"""

    def __init__(self):
        """Initiliazes intents and synced settings across bot instances"""

        super().__init__(intents=intents)
        self.synced = False # Syncs views only once
        self.added = False # Syncs command tree only once

    async def on_ready(self):
        """Syncs settings across different instances of the bot"""

        await self.wait_until_ready()

        if not self.added:
            self.add_view(StandardView())
            self.addded = True

        # Syncs tree commands
        if not self.synced:
            await tree.sync()
            self.synced = True

        print(f"Say hi to {self.user}")

class StandardView(discord.ui.View):
    """"""

    def __init__(self) -> None:
        """Sets the timeout for the View to never time out"""
        super().__init__(timeout=None)

    @discord.ui.button(custom_id='roll_button', label='Roll Again', style=discord.ButtonStyle.blurple)
    async def roll_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Let's users start another roll"""
        await interaction.response.send_message(embed=embed_maker(interaction), view=StandardView())

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = bot_client()
tree = discord.app_commands.CommandTree(client)

# Simgle command that can be called with /roll
@tree.command(name='roll', description='Roll a die.', guild=discord.Object(os.getenv("DISCORD_GUILD")))
async def roll(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed_maker(interaction), view=StandardView())

# # Command with options at the end
# GreetingTime = Enum(value='GreetingTime', names=['MORNING', 'AFTERNOON', 'EVENING', 'NIGHT'])
# @tree.command(description='Respond according to the period of the day.', guild=discord.Object(os.getenv("DISCORD_GUILD")))
# @discord.app_commands.describe(period='Period of the day')
# async def greet_user_time_of_the_day(interaction: discord.Interaction, period: GreetingTime):
#     user = interaction.user.id
#     await interaction.response.send_message(f'Good {period.name.title()}, <@{user}>!')
#     return


@client.event
async def on_message(message):

    # Checks if the message is from the bot itself to prevent spamming
    if message.author == client.user:
        return
    
    if message.content == 'Hello!':
        await message.channel.send("Hello there!")

    if message.content == '$roll':
        await message.channel.send(embed=embed_maker(client), view=StandardView())
    
    if message.content == '$character':
        await message.channel.send(embed=roll_character())

client.run(os.environ.get('DISCORD_TOKEN'))
