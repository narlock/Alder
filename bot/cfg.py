"""
cfg.py
author: narlock

cfg.py is the configuration loader for AlderBot. It provides a constant interface
for accessing the configurations that are required.
"""

import os
import yaml
import discord

# Obtain the discord bot token from file on local computer system
def read(file_name):
    path = os.getenv("HOME") + os.sep + "Documents" + os.sep + "narlock" + os.sep + "Alder" + os.sep + file_name
    with open(path, "r") as file:
        contents = file.read()
        return contents

# Configure to your token file
TOKEN = read('token')

# Import config.yaml into the project
def read_config(file_path):
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as error:
            print(f"Error reading the YAML file: {error}")
            return None

# Configure to your configuration file
CONFIG = read_config('config.yaml')

"""
Access configuration values, examples:
print(CONFIG)
print(CONFIG['mysql]) # returns the mysql object
print(CONFIG['mysql']['user']) # returns the user value

Import inside of other classes by using `import cfg`
"""

# Initialize constants for mysql connection
MYSQL = CONFIG['mysql']
MYSQL_USER = MYSQL['user']
MYSQL_PASSWORD = MYSQL['password']
MYSQL_HOST = MYSQL['host']
MYSQL_DATABASE = MYSQL['database']

# Initialize log level constant
LOG_LEVEL = CONFIG['log.level']

# Initialize Alder API URL
ALDER_API_URL = CONFIG['api']['url']

# Initialize Rogue Boss URL
ROGUE_BOSS_URL = CONFIG['rogueboss']['url']

# Initialize Discord properties
DISCORD = CONFIG['discord']
DISCORD_ALDER_IMAGE_URL = DISCORD['alder.image']
DISCORD_SERVER_ID = DISCORD['server']

# Channels
DISCORD_CHANNELS = DISCORD['channels']
ANNOUNCEMENT_CHANNEL_ID = DISCORD_CHANNELS['announcement']
RULES_CHANNEL_ID = DISCORD_CHANNELS['rules']
ROLE_CHANNEL_ID = DISCORD_CHANNELS['role']
ACTIVITY_CHANNEL_IDS = DISCORD_CHANNELS['activity']
INFO_CHANNEL_ID = DISCORD_CHANNELS['info']

# Roles
DISCORD_ROLES = DISCORD['roles']
DEEP_FOCUS_ROLE_ID = DISCORD_ROLES['deepfocus']
STREAM_ROLE_ID = DISCORD_ROLES['stream']
YOUTUBE_ROLE_ID = DISCORD_ROLES['youtube']
FOREST_ROLE_ID = DISCORD_ROLES['forest']
BOOK_ROLE_ID = DISCORD_ROLES['book']

STAFF_ROLE_IDS = DISCORD_ROLES['staff']
ADMIN_ROLE_ID = STAFF_ROLE_IDS['admin']
MOD_ROLE_ID = STAFF_ROLE_IDS['mod']

SPONSOR_ROLE_IDS = DISCORD_ROLES['sponsor']
SUPPORTER_ROLE_ID = SPONSOR_ROLE_IDS['supporter']
BOOSTER_ROLE_ID = SPONSOR_ROLE_IDS['booster']
YOUTUBE_MEMBER_ROLE_ID = SPONSOR_ROLE_IDS['youtube']
SPECIAL_ROLE_IDS = DISCORD_ROLES['special']

ACTIVITY_ROLES = DISCORD_ROLES['activity']
LEVEL_1_ACTIVITY_ROLE = ACTIVITY_ROLES['level1']
LEVEL_2_ACTIVITY_ROLE = ACTIVITY_ROLES['level2']
LEVEL_3_ACTIVITY_ROLE = ACTIVITY_ROLES['level3']
LEVEL_4_ACTIVITY_ROLE = ACTIVITY_ROLES['level4']
LEVEL_5_ACTIVITY_ROLE = ACTIVITY_ROLES['level5']
LEVEL_6_ACTIVITY_ROLE = ACTIVITY_ROLES['level6']

COLOR_ROLES = DISCORD_ROLES['color']

# Commands
DISCORD_COMMANDS = DISCORD['command.id']
DEEP_FOCUS_COMMAND_ID = DISCORD_COMMANDS['deepfocus']
PROFILE_COMMAND_ID = DISCORD_COMMANDS['profile']
ROGUE_BOSS_COMMAND_ID = DISCORD_COMMANDS['rogueboss']
SHOP_COMMAND_ID = DISCORD_COMMANDS['shop']
SHOP_COLOR_COMMAND_ID = DISCORD_COMMANDS['shopcolor']
SHOP_EMBED_COMMAND_ID = DISCORD_COMMANDS['shopembed']
HELP_COMMAND_ID = DISCORD_COMMANDS['help']
RULES_COMMAND_ID = DISCORD_COMMANDS['rules']
ACHIEVEMENTS_COMMAND_ID = DISCORD_COMMANDS['achievements']
ROLL_COMMAND_ID = DISCORD_COMMANDS['roll']
EIGHTBALL_COMMAND_ID = DISCORD_COMMANDS['eightball']
MOTIVATION_COMMAND_ID = DISCORD_COMMANDS['motivation']
KANBAN_COMMAND_ID = DISCORD_COMMANDS['kanban']
TODO_COMMAND_ID = DISCORD_COMMANDS['todo']
TOP_COMMAND_ID = DISCORD_COMMANDS['top']
TRIVIA_COMMAND_ID = DISCORD_COMMANDS['trivia']
DAILY_COMMAND_ID = DISCORD_COMMANDS['daily']

# Emotes
CUSTOM_EMOJIS = DISCORD['emoji']
STAFF_EMOJI = CUSTOM_EMOJIS['staff']
SUPPORTER_EMOJI = CUSTOM_EMOJIS['supporter']
BOOSTER_EMOJI = CUSTOM_EMOJIS['booster']
ALUMNI_EMOJI = CUSTOM_EMOJIS['alumni']

# Rules
RULES = DISCORD['rules']

# Constant discord embeds
EMBED_FOOTER_STRING = 'Powered by **[@narlockdev](https://twitter.com/narlockdev)**'
class ErrorEmbed():
    @staticmethod
    def message(msg: str) -> discord.Embed:
        """
        Generates a Discord embed signaling that an error occurred.
        The {msg} parameter is used to specify the error.
        """
        embed = discord.Embed(title='AlderBot Error Occurred', color=0xff0000)
        embed.set_thumbnail(url=DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name="An error occurred\n\u200b\n", value=f"{msg}", inline=False)
        embed.add_field(name='\u200b', value=EMBED_FOOTER_STRING, inline=False)
        return embed
    
    @staticmethod
    def notokens(tokens: int, amount: int) -> discord.Embed:
        """
        A common Discord embed signaling that a Discord member
        does not have enough tokens to perform the operation.
        
        The {tokens} parameter is the amount of tokens the calling
        member currently owns. The {amount} parameter is the amount
        of tokens it costs to perform the operation.
        """
        embed = discord.Embed(title=f'You do not have enough tokens!', color=0xff3a40)
        embed.set_thumbnail(url=DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='\u200b', value=f'It costs `{amount}` :coin: tokens to perform this operation.\n→ You currently own `{tokens}` tokens.', inline=False)
        embed.add_field(name='\u200b', value=f'You can earn :coin: tokens by spending focus time\nin a dedicated focus room!\n→ To check your amount of tokens, use </profile:{PROFILE_COMMAND_ID}>.', inline=False)
        embed.add_field(name='\u200b', value=EMBED_FOOTER_STRING, inline=False)
        return embed
    
NO_PROFILE_EMBED = ErrorEmbed.message("Member does not have a profile!\nMember has to have joined a focus room to have a profile.")
INVALID_COLOR_EMBED = ErrorEmbed.message('Invalid color option was entered.\nEnter an integer between `1` and `16`.')

# Other constants
ROLES_MESSAGE = """
# Notification Roles
Click to toggle notifications from any of the following activities!
"""
DEEP_FOCUS_MESSAGE = """
# Deep Focus Mode
Entering deep focus will empower you to be free from distractions. This means that you will not have access to read chat channels or send messages. The goal of this is so that you can toggle when you want to be in deep focus, while also displaying to other members that you do not want to be disturbed at the current moment. By clicking the `🔴 Toggle Deep Focus` button below, you will activate deep focus, and the Deep Focus role will be added to your profile. By clicking again, this role will be removed and you will no longer be in deep focus.
"""

MONTHS = [
    "MissingNo",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]