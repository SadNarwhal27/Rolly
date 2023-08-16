import random
import discord
import json

def _roll_dice(num_of_dice, dice_sides):
    """Roll a set number of dice with specific number of sides"""

    rolls = []

    for _ in range(num_of_dice):
        temp_roll = random.randint(1, dice_sides)
        rolls.append(temp_roll)

    return rolls

def _load_responses():
    """Loads in the responses data"""

    with open('responses.json', encoding='utf8') as file:
        all_responses = json.load(file)
        file.close()
    return all_responses

def _get_response(response_type: str) -> str:
    """Chooses a random response"""

    chosen_response = random.choice(_load_responses()[response_type])
    return chosen_response


def embed_maker(interaction: discord.Interaction) -> discord.Embed:
    """Creates a Discord embed that can be passed into a message"""

    embed = discord.Embed(
        title=f"{_get_response('start')} {_roll_dice(1, 20)[0]}", 
        color=0xff0000,)
    embed.set_author(name=interaction.user.global_name, icon_url=interaction.user.display_avatar)

    return embed

def roll_character():
    rolls = []
    for _ in range(7):
        temp_rolls = _roll_dice(4, 6)
        temp_rolls.remove(min(temp_rolls))
        rolls.append(str(sum(temp_rolls)))
    message = f"{_get_response('stats')}{', '.join(rolls[0:6])}"
    
    embed = discord.Embed(\
        title=message,
        description= _get_response('mulligans').format(rolls[6]),
        color=0xff0000)
    return embed
        
