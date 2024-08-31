"""
rb.py
author: narlock

Rogue Boss: https://github.com/narlock/RogueBoss is a boss battle simulator for building
commuinities. It is mainly used for study stream purposes, where the display window appears
on the live stream. Viewers can play Rogue Boss and see their character attack the boss.

The following code (rb.py) provides a Discord interface for interacting with Rogue Boss.
"""

import cfg
import discord
import requests
import json
import traceback

from tools.log import Logger
from client.alder.interface.user_client import UserClient
from client.alder.interface.rogueboss_client import RbClient

RB_MODELS = ['TRINITY', 'ANT']

class RogueBossTypeChooser(discord.ui.View):
    """
    RogueBossTypeChooser is the Discord view of the Rogue Boss dialog for selecting a type.
    This view will be used when the user is not registered on the backend database. It displays
    an initial message along side a button corresponding to each type in Rogue Boss. When a user
    clicks on one of the type buttons, they will be assigned to the type on the backend database.
    The view will update to reflect the user's decision.
    """
    def __init__(self, embed: discord.Embed, user_id: int):
        super().__init__(timeout=None)
        self.embed = embed
        self.user_id = user_id
        self.welcome_msg = '''
            Welcome to ***Rogue Boss***!

            *Rogue Boss* is a "boss battle" simulator for building communities. Like playing a video game, members of the Discord server can work together to defeat the current boss! Rogue Boss events are active while narlock is study streaming. When active, members of the Discord server can utilize `/rb` to attack the boss! It costs `25` :coin: tokens per attack. Once a boss is defeated, all contributors will receive XP and level up! Leveling up will allow you to deal more damage to future bosses. When a boss is defeated, a new, stronger one will take its place.

            Your time has now come!\nChoose which Rogue Boss type you would like to be:
        '''
        self.embed.set_field_at(0, name='\u200b', value=self.welcome_msg, inline=False)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if the user who clicked the button is the same as the user who initiated the game."""
        return interaction.user.id == self.user_id

    @discord.ui.button(label='🔥 FIRE', style=discord.ButtonStyle.blurple)
    async def option_fire(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'You chose 🔥 **FIRE**!\n\nYour attacks will do extra damage to 🪨 **EARTH** bosses!\nBeware of 💧 **WATER** bosses, your attacks will do half the damage!', inline=False)
        RbClient.create_rogue_boss_user(interaction.user.id, 'FIRE')
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='💧 WATER', style=discord.ButtonStyle.blurple)
    async def option_water(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'You chose 💧 **WATER**!\n\nYour attacks will do extra damage to 🔥 **FIRE** bosses!\nBeware of 🪨 **EARTH** bosses, your attacks will do half the damage!', inline=False)
        RbClient.create_rogue_boss_user(interaction.user.id, 'WATER')
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🪨 EARTH', style=discord.ButtonStyle.blurple)
    async def option_earth(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'You pressed 🪨 **EARTH**\n\nYour attacks will do extra damage to 💧 **WATER** bosses!\nBeware of 🔥 **FIRE** bosses, your attacks will do half the damage!', inline=False)
        RbClient.create_rogue_boss_user(interaction.user.id, 'EARTH')
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)
        
    @discord.ui.button(label='🔮 PSYCHIC', style=discord.ButtonStyle.blurple)
    async def option_psychic(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'You pressed 🔮 **PSYCHIC**\n\nYour attacks will do extra damage to 🌑 **DARK** bosses!\nBeware of 💫 **LIGHT** bosses, your attacks will do half the damage!', inline=False)
        RbClient.create_rogue_boss_user(interaction.user.id, 'PSYCHIC')
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label='💫 LIGHT', style=discord.ButtonStyle.blurple)
    async def option_light(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'You pressed 💫 **LIGHT**\n\nYour attacks will do extra damage to 🔮 **PSYCHIC** bosses!\nBeware of 🌑 **DARK** bosses, your attacks will do half the damage!', inline=False)
        RbClient.create_rogue_boss_user(interaction.user.id, 'LIGHT')
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🌑 DARK', style=discord.ButtonStyle.blurple)
    async def option_dark(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'You pressed 🌑 **DARK**\n\nYour attacks will do extra damage to 💫 **LIGHT** bosses!\nBeware of 🔮 **PSYCHIC** bosses, your attacks will do half the damage!', inline=False)
        RbClient.create_rogue_boss_user(interaction.user.id, 'DARK')
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

class RogueBoss():
    def __init__(self):
        self.info_msg = '''
            Welcome to ***Rogue Boss***!

            *Rogue Boss* is a "boss battle" simulator for building communities. Like playing a video game, members of the Discord server can work together to defeat the current boss! Rogue Boss events are active while narlock is study streaming. When active, members of the Discord server can utilize `/rb` to attack the boss! It costs `25` :coin: tokens per attack. Once a boss is defeated, all contributors will receive XP and level up! Leveling up will allow you to deal more damage to future bosses. When a boss is defeated, a new, stronger one will take its place.

            Commands:
            • To attack, use `/rb`.
            • To view your Rogue Boss statistics, use `/rb stats`
            • To view type charting in Rogue Boss, use `/rb type`
            • To change your model, use `/rb model 0` or `/rb model 1`
            • To view the top Rogue Boss members, user `/top rb`
        '''
        self.type_msg = '''
            Certain types in Rogue Boss have advantages over one another.

            🔥 **FIRE** is weak to **WATER**, but super effective aganist **EARTH**.
            💧 **WATER** is weak to **EARTH**, but super effective against **FIRE**.
            🪨 **EARTH** is weak to **FIRE**, but super effective against **WATER**.
            🔮 **PSYCHIC** is weak to **LIGHT**, but super effective against **DARK**.
            💫 **LIGHT** is weak to **DARK**, but super effective against **PSYCHIC**.
            🌑 **DARK** is weak to **PSYCHIC**, but super effective against **LIGHT**.

            Based on typing, if your type is weak to the boss type, you will deal half of the damage you roll. If your type is super effective, your attack will do double the damage!
        '''

    def initial(self):
        embed = discord.Embed(title=f"Rogue Boss", color=0xffa500)
        embed.add_field(name='\u200b', value='', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def show_stats(self, interaction: discord.Interaction, user):
        Logger.debug(f'Inside of show_stats for {interaction.user.name}')

        # Fetch the caller's hex code
        color = UserClient.get_discord_user_embed_color(interaction.user.id)

        embed = discord.Embed(title=f'RogueBoss Statistics for {interaction.user.name}', color=color)
        try:
            embed.set_thumbnail(url=f'{interaction.user.avatar.url}')
        except Exception as e:
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)

        # Setting rbtype, calculating level, and setting xp due to Python 3.11 limitations
        rbtype = self.get_type_string(user['rbtype'])
        xp = user['xp']
        level = self.calculate_level(xp)

        embed.add_field(name='\u200b', value=f':small_blue_diamond: Type: {rbtype}\n:small_blue_diamond: Level: {level}\n:small_blue_diamond: XP: {xp}', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed

    def show_info(self):
        embed = discord.Embed(title='Rogue Boss', color=0xffa500)
        embed.add_field(name='\u200b', value=self.info_msg)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def show_type(self):
        embed = discord.Embed(title='Rogue Boss', color=0xffa500)
        embed.add_field(name='\u200b', value=self.type_msg)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed

    def get_type_string(self, input_str):
        type_mapping = {
            "FIRE": "🔥 FIRE",
            "WATER": "💧 WATER",
            "EARTH": "🪨 EARTH",
            "PSYCHIC": "🔮 PSYCHIC",
            "LIGHT": "💫 LIGHT",
            "DARK": "🌑 DARK"
        }
        return type_mapping.get(input_str.upper(), "Unknown Type")
    
    def calculate_level(self, xp):
        Logger.debug(f'Calculating level where xp is {xp}')
        level = 1 if xp < 9 else round(xp ** 0.317)
        return level

    def play_rb(self, interaction: discord.Interaction, user):
        # Obtain ping to see if Rogue Boss is up!
        url = cfg.ROGUE_BOSS_URL
        try:
            Logger.debug('Pinging Rogue Boss Server...')
            ping_response = requests.get(url, timeout=1)
        except Exception as e:
            Logger.warn('Rogue Boss Server not available...')
            message = 'Rogue Boss event is **NOT** active at this time.\n→ The event will be active during the __next study stream__!'
            embed = discord.Embed(title=f"Rogue Boss")
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
            embed.add_field(name='\u200b', value=f'{message}', inline=False)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed

        # Check tokens to see if the user can play Rogue Boss
        user_tokens = UserClient.get_user_tokens(interaction.user.id)

        if user_tokens < 25:
            # User cannot play rogue boss
            embed = cfg.ErrorEmbed.notokens(user_tokens, 25)
            return embed
        
        """
        Play Rogue Boss is valid after confirming Rogue Boss server is
        available and user has enough tokens.
        """

        # Subtract tokens for play
        UserClient.subtract_tokens_user(interaction.user.id, 25)

        # Prepare request to LAN server and send
        model_index = user['model'] if user['model'] is not None else 0
        payload = {'id': user['user_id'], 'name': interaction.user.name, 'type': user['rbtype'], 'model': RB_MODELS[model_index], 'weapon': 1, 'powerUp': 1, 'exp': user['xp']}
        response = requests.post(url, json=payload)
        Logger.debug(f'Response from Rogue Boss Server: {response.status_code} on {url}.')

        if response.status_code == 200:
            body = json.loads(response.text)
            Logger.debug(f'Rogue Boss response body: {body}')

            # Check if the boss was slain, if it was, print out that message and that the user slayed the boss!
            if(body['slain'] is True):
                # Update each row of the database where the damageList contains the user id, update XP for each as well
                # Return embed with results of defeating the boss.
                top_contributors_set = self.update_rbuser_xp(body)
                
                guild = interaction.guild
                usernames_and_damage = []

                # get each username of top contributor
                if guild:
                    for user_id, damage in top_contributors_set:
                        member = guild.get_member(int(user_id))
                        username = member.name if member else "Narlock User"
                        usernames_and_damage.append((username, damage))

                # Construct the concatenated string
                sorted_list = sorted(usernames_and_damage, key=lambda x: x[1], reverse=True)
                result_string = ""
                for username, damage in sorted_list:
                    result_string += f":small_orange_diamond: **{username}**: {damage} damage, **{damage/2}** XP earned!\n"

                note = body['note']
                boss_name = body['boss']['name']

                embed = discord.Embed(title=f"Rogue Boss")
                embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
                embed.color = discord.Color.blue()

                embed.add_field(name='\u200b', value=f'**{interaction.user.name}** dealt the final blow to the {boss_name}!', inline=False)
                embed.add_field(name='\u200b', value='', inline=False)
                embed.add_field(name='Top Boss Contributors', value=result_string, inline=False)

                embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
                return embed
            else:
                # Otherwise, reply back with the value of "Note" and the amount of total damage the user has done
                note = body['note']
                boss_name = body['boss']['name']
                health_remaining = body['boss']['health']

                embed = discord.Embed(title=f"Rogue Boss")
                embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
                if 'missed' in note:
                    embed.color = discord.Color.red()
                elif 'Critical hit!' in note:
                    embed.color = discord.Color.gold()
                else:
                    embed.color = discord.Color.green()

                embed.add_field(name='\u200b', value=f'{note}')
                embed.add_field(name='\u200b', value=f'{boss_name} has `{health_remaining}` health remaining!\n→ You now have {user_tokens - 25} tokens.', inline=False)
                embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
                return embed
        else:
            # Unexpected error
            embed = cfg.ErrorEmbed.message("Unexpected error occurred. We are sorry for the inconvenience.")
            return embed
        
    def update_rbuser_xp(self, response_body):
        """
        Given a JSON response body from Rogue Boss, update Rogue Boss user
        experience.
        
        Return the top Rogue Boss contributors (those with most xp earned
        based on the JSON response)
        """
        top_contributors_set = set()

        damage_list = response_body.get("boss", {}).get("damageList", [])
        contributors = []

        for item in damage_list:
            user_id = item.get("id")
            damage = item.get("damage")
            xp_gained = damage / 2

            RbClient.add_xp_to_rogue_boss_user(user_id, xp_gained)
            contributors.append({"user_id": user_id, "damage": damage})

        contributors.sort(key=lambda x: x["damage"], reverse=True)
        top_contributors = contributors[:5]

        if len(top_contributors) > 0:
            for contributor in top_contributors:
                top_contributors_set.add((contributor['user_id'], contributor['damage']))

        return top_contributors_set