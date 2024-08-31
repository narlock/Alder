"""
top.py
author: narlock

App interface for retrieiving leaderboard information.
"""

import cfg
import discord

from tools.log import Logger
from client.alder.interface.monthtime_client import MonthTimeClient
from client.alder.interface.dailytime_client import DailyTimeClient
from client.alder.interface.user_client import UserClient
from client.alder.interface.rogueboss_client import RbClient
from client.alder.interface.streak_client import StreakClient

PLACES = [':first_place: First', ':second_place: Second', ':third_place: Third']
HONORABLE_MENTIONS_NAME = ':mega: Honorable Mentions'

class Top():
    def display_top(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the top users on the server, handles different counts of top users.
        """
        Logger.debug(f"Generating top embed. Requested by {interaction.user.name}")
        
        # Retrieve top monthtime users
        top_monthtime_users = MonthTimeClient.get_top_10_stime_users_current_month()

        # Return no members on leaderboard if none are found
        if not top_monthtime_users:
            embed = discord.Embed(title='Focus Leaderboard :trophy:', description="No members on the leaderboard this month.", color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed

        # Create the top month leaderboard embed
        embed = discord.Embed(title='Focus Leaderboard :trophy:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_monthtime_users):
            # Obtain the member from their user_id
            member = interaction.guild.get_member(user['user_id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumbnail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')

            # Convert user month stime to hours
            month_time = user['stime'] // 3600

            if index < 3:
                # Add dedicated embed field if in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** ({month_time} hrs)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** ({month_time} hrs)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)

        # Add information to embed and return
        embed.add_field(name='\u200b', value=f':small_blue_diamond: Leaderboard resets monthly relative to UTC.\n:small_blue_diamond: At the *end of the month*,\n→ :first_place: **First** gains 200 :coin: & <@&{cfg.SUPPORTER_ROLE_ID}> (1 mth)\n→ :second_place: **Second** gains 100 :coin:\n→ :third_place: **Third** gains 50 :coin:', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def display_top_daily(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the top users on the server for today, handles different counts of top users.
        """
        Logger.debug(f"Generating top daily embed. Requested by {interaction.user.name}")
        
        # Retrieve top monthtime users
        top_dailytime_users = DailyTimeClient.get_top_10_stime_users_today()

        # Return no members on leaderboard if none are found
        if not top_dailytime_users:
            embed = discord.Embed(title='Daily Focus Leaderboard :hourglass:', description="No members on the leaderboard this month.", color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed

        # Create the top daily leaderboard embed
        embed = discord.Embed(title='Daily Focus Leaderboard :hourglass:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_dailytime_users):
            # Obtain the member from their user_id
            member = interaction.guild.get_member(user['user_id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumbnail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')

            # Convert user daily stime to hours
            daily_time = user['stime'] // 3600

            if index < 3:
                # Add dedicated embed field if in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** ({daily_time} hrs)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** ({daily_time} hrs)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)

        # Add information to embed and return
        embed.add_field(name='\u200b', value=f':small_blue_diamond: Leaderboard resets daily relative to UTC.', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def display_top_trivia(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the top trivia users on the server, handles different counts of top users.
        """
        Logger.debug(f'Generating top trivia embed. Requested by {interaction.user.name}')

        # Retrieve top trivia users
        top_trivia_users = UserClient.search_top_trivia_users()

        # Return no members on leaderboard if none are found
        if not top_trivia_users:
            embed = discord.Embed(title='Trivia Leaderboard :trophy:', description="No members on the trivia leaderboard.", color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed
        
        # Create the top trivia leaderboard embed
        embed = discord.Embed(title='Trivia Leaderboard :joystick:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_trivia_users):
            # Obtain the mmeber from their user_id
            member = interaction.guild.get_member(user['id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumbnail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')

            user_trivia = user['trivia']
            if index < 3:
                # Add dedicated embed field if member is in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** ({user_trivia} correct answers)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** ({user_trivia} correct answers)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)
        
        # Add information to embed and return
        embed.add_field(name='\u200b', value=f':small_blue_diamond: Leaderboard is based on amount of trivia wins!\n:small_blue_diamond: Play trivia using the </trivia:{cfg.TRIVIA_COMMAND_ID}> command (Costs 25 tokens)', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def display_top_rb(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the top rogue boss users on the server, handles different counts of top users.
        """
        Logger.debug(f'Generating top rogue boss embed. Requested by {interaction.user.name}')

        # Retrieve top rogue boss users
        top_rogueboss_users = RbClient.get_top_10_rogue_boss_users()

        # Return no members on leaderboard if none are found
        if not top_rogueboss_users:
            embed = discord.Embed(title='Rogue Boss Leaderboard :crossed_swords:', description="No members on the Rogue Boss leaderboard.", color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed
        
        # Create the top Rogue Boss users leaderboard embed
        embed = discord.Embed(title='Rogue Boss Leaderboard :crossed_swords:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_rogueboss_users):
            # Obtain the member from their user_id
            member = interaction.guild.get_member(user['user_id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            # Get user Rogue Boss level and XP
            rb_level, rb_xp = RbClient.get_rogue_boss_level_and_xp(member.id)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumnbail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')
            
            if index < 3:
                # Add embed field if the member is in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** (Level {rb_level}, {rb_xp} XP)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** (Level {rb_level}, {rb_xp} XP)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)
        
        # Add information to embed and return
        embed.add_field(name='\u200b', value=f':small_blue_diamond: Leaderboard is based on Rogue Boss Level!\n:small_blue_diamond: Play Rogue Boss when stream is active by using </rb:{cfg.ROGUE_BOSS_COMMAND_ID}> (Costs 25 tokens)', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def display_top_all(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the top users on the server, handles different counts of top users.
        """
        Logger.debug(f"Generating top embed. Requested by {interaction.user.name}")
        
        # Retrieve top monthtime users
        top_stime_users = UserClient.search_top_stime_users()

        # Return no members on leaderboard if none are found
        if not top_stime_users:
            embed = discord.Embed(title='Focus Leaderboard :trophy:', description="No members on the leaderboard this month.", color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed

        # Create the top month leaderboard embed
        embed = discord.Embed(title='All-Time Focus Leaderboard :trophy:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_stime_users):
            # Obtain the member from their user_id
            member = interaction.guild.get_member(user['id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumbnail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')

            # Convert user month stime to hours
            stime = user['stime'] // 3600

            if index < 3:
                # Add dedicated embed field if in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** ({stime} hrs)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** ({stime} hrs)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)

        # Add information to embed and return
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def display_top_streak(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the users with the highest current streaks on the server, handles different counts of top users.
        """
        Logger.debug(f'Generating top current streak embed. Requested by {interaction.user.id}')

        # Retrieve top current streak users
        top_streak_users = StreakClient.get_top_10_current_streak_users()

        # Return no members on leaderboard if none are found
        if not top_streak_users:
            embed = discord.Embed(title='Current Streak Leaderboard :calendar:', description='No members on the Current Streak leaderboard', color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed
        
        # Create the highest streaks leaderboard embed
        embed = discord.Embed(title='Current Streak Leaderboard :calendar:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_streak_users):
            # Obtain the member from their user_id
            member = interaction.guild.get_member(user['user_id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumbnail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')

            user_current_streak = user['current_streak']
            if index < 3:
                # Add dedicated embed field if in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** ({user_current_streak} days)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** ({user_current_streak} days)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)

        # Add information to embed and return
        embed.add_field(name='\u200b', value=f':small_blue_diamond: Streaks indicate consecutive daily participation.', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed

    def display_top_streaks_all_time(self, interaction: discord.Interaction) -> discord.Embed:
        """
        Generates the embed for the users with the highest current streaks on the server, handles different counts of top users.
        """
        Logger.debug(f'Generating top current streak embed. Requested by {interaction.user.id}')

        # Retrieve top current streak users
        top_streak_users = StreakClient.get_top_10_highest_streak_users()

        # Return no members on leaderboard if none are found
        if not top_streak_users:
            embed = discord.Embed(title='Highest Streak Leaderboard :calendar:', description='No members on the Highest Streak leaderboard', color=0xffa500)
            embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
            return embed
        
        # Create the highest streaks leaderboard embed
        embed = discord.Embed(title='Highest Streak Leaderboard :calendar:', color=0xffa500)
        honorable_mentions = []

        for index, user in enumerate(top_streak_users):
            # Obtain the member from their user_id
            member = interaction.guild.get_member(user['user_id'])

            # Set the username based on the value of the member.
            username = self.get_username(member)

            if member is not None and index == 0:
                # Add the member's avatar as the embed thumbnail
                avatar_url = self.get_top_url(member)
                embed.set_thumbnail(url=f'{avatar_url}')

            user_highest_streak = user['highest_streak_achieved']
            if index < 3:
                # Add dedicated embed field if in first, second, or third place
                embed.add_field(name=PLACES[index], value=f'**{username}** ({user_highest_streak} days)', inline=False)
            else:
                # Add honorable mention
                honorable_mentions.append(f'**{username}** ({user_highest_streak} days)')

        # If there are honorable mentions, add them to the embed
        if honorable_mentions:
            embed.add_field(name=HONORABLE_MENTIONS_NAME, value='\n'.join(honorable_mentions), inline=False)

        # Add information to embed and return
        embed.add_field(name='\u200b', value=f':small_blue_diamond: Highest streaks indicate consecutive daily participation on record.', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def get_username(self, member: discord.Member):
        if member is None:
            # TODO Remove member from database?
            # This occurs if member leaves the server
            return "Alder"
        else:
            return member.name
        
    def get_top_url(self, member: discord.Member):
        if member is None:
            # TODO Remove member from database?
            # This occurs if member leaves the server
            return cfg.DISCORD_ALDER_IMAGE_URL
        else:
            return member.avatar.url
