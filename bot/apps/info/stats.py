"""
stats.py
author: narlock

Interface to display and retrieve profile statistics.
"""

import cfg
import discord
import math
import traceback
import json

from tools.log import Logger
from apps.info.achievement import Achievements
from client.alder.interface.user_client import UserClient
from client.alder.interface.monthtime_client import MonthTimeClient
from client.alder.interface.dailytime_client import DailyTimeClient
from client.alder.interface.rogueboss_client import RbClient
from client.alder.interface.accomplishment_client import AccomplishmentClient
from client.alder.interface.streak_client import StreakClient

class Stats():
    def __init__(self, achievements: Achievements):
        self.achievements = achievements

    def create_profile_embed(self, interaction: discord.Interaction, user: discord.User = None):
        """
        Create embed for discord user profile.
        """
        if user is None:
            # Interaction member is caller
            calling_user = interaction.user
        else:
            # Provided user is caller
            calling_user = user

        # See if user is special role
        user_roles = [role.id for role in calling_user.roles]
        Logger.debug(f'user {calling_user.name}\'s roles: {user_roles}')
        staff_id = cfg.STAFF_ROLE_IDS['group']
        booster_id = cfg.BOOSTER_ROLE_ID
        supporter_id = cfg.SUPPORTER_ROLE_ID
        alumni_id = cfg.SPECIAL_ROLE_IDS[0]

        special_emote = ''
        if staff_id in user_roles:
            special_emote += f'<:Staff:{cfg.STAFF_EMOJI}>'
        if supporter_id in user_roles:
            special_emote += f'<:Supporter:{cfg.SUPPORTER_EMOJI}>'
        if booster_id in user_roles:
            special_emote += f'<:Booster:{cfg.BOOSTER_EMOJI}>'
        if alumni_id in user_roles:
            special_emote += f'<:Alumni:{cfg.ALUMNI_EMOJI}>'
        
        # Create user if they do not exist in DB
        UserClient.create_user_if_dne(calling_user.id)

        # Fetch the statistics for the profile
        month_stime = MonthTimeClient.get_stime_value_for_user_current_month(calling_user.id) // 3600
        daily_stime = DailyTimeClient.get_stime_value_for_user_today(calling_user.id) // 3600
        user_stime = UserClient.get_user_stime(calling_user.id) // 3600
        user_tokens = UserClient.get_user_tokens(calling_user.id)
        user_trivia = UserClient.get_user_trivia(calling_user.id)
        rb_level = RbClient.get_rogue_boss_level(calling_user.id)
        accomplishments = AccomplishmentClient.get_accomplishments_for_user_content(calling_user.id)

        # Get achievement information from Achievements module
        achievements = self.achievements.get_earned_achievements(calling_user.id)
        earned_achievements = achievements[0]
        total_achievements = achievements[1]

        # Upsert streak if applicable, then retrieve streak
        StreakClient.set_streak_for_user(calling_user.id)
        streak_response = StreakClient.get_streak_for_user(calling_user.id)
        if streak_response is not None:
            streak_no = json.loads(streak_response.text)['current_streak']
            if streak_no == 0:
                streak = ''
            else: 
                streak = f'🔥 **Activity Streak:** {streak_no}'
        else:
            streak = ''

        # Create Discord Embed for Profile
        embed = discord.Embed(title=f'**{calling_user.name}** {special_emote}', description=streak, color=UserClient.get_discord_user_embed_color(calling_user.id))
        try:
            embed.set_thumbnail(url=f'{calling_user.avatar.url}')
        except Exception as e:
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='General', value=f':hourglass: **Today\'s Focus:** {daily_stime} hrs\n:calendar: **Month Focus:** {month_stime} hrs\n:star: **Total Focus:** {user_stime} hrs\n:coin: **Tokens:** {user_tokens}', inline = False)
        embed.add_field(name='Achievements', value=f'🎉 **{earned_achievements}/{total_achievements}**', inline=False)
        embed.add_field(name='Arcade', value=f':question: **Trivia Questions Answered:** {user_trivia}\n:crossed_swords: **Rogue Boss Level:** {rb_level}')

        if accomplishments:
            combined_string = "\n".join(accomplishments)
            embed.add_field(name='Notable Accomplishments', value=combined_string, inline=False)

        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed