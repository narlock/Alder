"""
achievement.py
author: narlock

Achievement interface for AlderBot.
"""

import cfg
import discord
import math
import json

from tools.log import Logger
from client.alder.interface.user_client import UserClient
from client.alder.interface.monthtime_client import MonthTimeClient
from client.alder.interface.achievement_client import AchievementClient
from client.alder.interface.streak_client import StreakClient
from client.alder.interface.rogueboss_client import RbClient

# Alder achievements
achievements = [
    {
        'id': 0,
        'title': 'Tenfold Tenacity',
        'desc': 'Accumulate 10 hours total of focus time.',
        'value': 10
    },
    {
        'id': 1,
        'title': 'Fifty-Hour Focus Feat',
        'desc': 'Accumulate 50 hours total of focus time.',
        'value': 50
    },
    {
        'id': 2,
        'title': 'Centennial Concentration',
        'desc': 'Accumulate 100 hours total of focus time.',
        'value': 100
    },
    {
        'id': 3,
        'title': 'Focused Endeavor',
        'desc': 'Accumulate 500 hours total of focus time.',
        'value': 500
    },
    {
        'id': 4,
        'title': 'Thousand-Hour Triumph',
        'desc': 'Accumulate 1000 hours total of focus time.',
        'value': 1000
    },
    {
        'id': 5,
        'title': 'Dual Millennia of Diligence',
        'desc': 'Accumulate 2000 hours total of focus time.',
        'value': 2000
    },
    {
        'id': 6,
        'title': 'Pentagram of Persistence',
        'desc': 'Accumulate 5000 hours total of focus time.',
        'value': 5000
    },
    {
        'id': 7,
        'title': 'Journey\'s Start',
        'desc': 'Achieve \"Novice\" focus role (Accumulate 3+ focus hours in a single month).',
        'value': 3
    },
    {
        'id': 8,
        'title': 'Continued Consistency',
        'desc': 'Achieve \"Intermediate\" focus role (Accumulate 10+ focus hours in a single month).',
        'value': 10
    },
    {
        'id': 9,
        'title': 'Advancing Focus',
        'desc': 'Achieve \"Advanced\" focus role (Accumulate 25+ focus hours in a single month).',
        'value': 25
    },
    {
        'id': 10,
        'title': 'Expertise Attained',
        'desc': 'Achieve \"Expert\" focus role (Accumulate 60+ focus hours in a single month).',
        'value': 60
    },
    {
        'id': 11,
        'title': 'Masterful Focus',
        'desc': 'Achieve \"Master\" focus role (Accumulate 100+ focus hours in a single month).',
        'value': 100
    },
    {
        'id': 12,
        'title': 'Narlock Focus Trailblazer',
        'desc': 'Achieve \"Narlock Scholar\" focus role (Accumulate 250+ focus hours in a single month).',
        'value': 250
    },
    {
        'id': 13,
        'title': 'Steadfast Starter',
        'desc': 'Obtain a study streak of 3 days (Join a study room for 3 days in a row).',
        'value': 3
    },
    {
        'id': 14,
        'title': 'Diligent Scholar',
        'desc': 'Obtain a study streak of 10 days (Join a study room for 10 days in a row).',
        'value': 10
    },
    {
        'id': 15,
        'title': 'Consistent Learner',
        'desc': 'Obtain a study streak of 30 days (Join a study room for 30 days in a row).',
        'value': 30
    },
    {
        'id': 16,
        'title': 'Study Room Centurion',
        'desc': 'Obtain a study streak of 100 days (Join a study room for 100 days in a row).',
        'value': 100
    },
    {
        'id': 17,
        'title': 'Yearlong Study Sentinel',
        'desc': 'Obtain a study streak of 365 days (Join a study room for 365 days in a row).',
        'value': 365
    },
    {
        'id': 18,
        'title': 'Knowledge Curator',
        'desc': 'Answer 25 Trivia questions correctly (via `/trivia`)',
        'value': 25
    },
    {
        'id': 19,
        'title': 'Mind Sharpshooter',
        'desc': 'Answer 50 Trivia questions correctly (via `/trivia`)',
        'value': 50
    },
    {
        'id': 20,
        'title': 'Wisdom Virtuoso',
        'desc': 'Answer 100 Trivia questions correctly (via `/trivia`)',
        'value': 100
    },
    {
        'id': 21,
        'title': 'Rogue Apprentice',
        'desc': 'Achieve level 3 in Rogue Boss (32+ XP)',
        'value': 32
    },
    {
        'id': 22,
        'title': 'Decade Attained',
        'desc': 'Achieve level 10 in Rogue Boss (1427+ XP)',
        'value': 1427
    },
    {
        'id': 23,
        'title': 'Quadrans Achiever',
        'desc': 'Achieve level 25 in Rogue Boss (25698+ XP)',
        'value': 25698
    },
    {
        'id': 24,
        'title': 'Half-Century Champion',
        'desc': 'Achieve level 50 in Rogue Boss (228837+ XP)',
        'value': 228837
    },
    {
        'id': 25,
        'title': 'Century Conqueror',
        'desc': 'Achieve level 100 in Rogue Boss (2037738+ XP)',
        'value': 2037738
    }
]

all_focus_achievements = [
    achievements[0],
    achievements[1],
    achievements[2],
    achievements[3],
    achievements[4],
    achievements[5],
    achievements[6]
]

month_focus_achievements = [
    achievements[7],
    achievements[8],
    achievements[9],
    achievements[10],
    achievements[11],
    achievements[12]
]

study_streak_achievements = [
    achievements[13],
    achievements[14],
    achievements[15],
    achievements[16],
    achievements[17]
]

trivia_achievements = [
    achievements[18],
    achievements[19],
    achievements[20]
]

rb_level_achievements = [
    achievements[21],
    achievements[22],
    achievements[23],
    achievements[24],
    achievements[25]
]

FULL = '█'
EMPTY = '-'
class Achievements:
    def get_progress_bar_by_percent(self, percent):
        if 0 <= percent < 10:
            return f"[{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 10 <= percent < 20:
            return f"[{FULL}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 20 <= percent < 30:
            return f"[{FULL}{FULL}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 30 <= percent < 40:
            return f"[{FULL}{FULL}{FULL}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 40 <= percent < 50:
            return f"[{FULL}{FULL}{FULL}{FULL}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 50 <= percent < 60:
            return f"[{FULL}{FULL}{FULL}{FULL}{FULL}{EMPTY}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 60 <= percent < 70:
            return f"[{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{EMPTY}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 70 <= percent < 80:
            return f"[{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{EMPTY}{EMPTY}{EMPTY}] {percent}%"
        elif 80 <= percent < 90:
            return f"[{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{EMPTY}{EMPTY}] {percent}%"
        elif 90 <= percent < 100:
            return f"[{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{EMPTY}] {percent}%"
        else:
            return f"[{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}{FULL}] {percent}%"

    def get_earned_achievements(self, user_id):
        # Ensure user is created on the database
        UserClient.create_user_if_dne(user_id)

        # Retrieve data for achievements
        all_focus_time = math.floor(UserClient.get_user_stime(user_id) / 3600) # in hours
        month_focus_time = math.floor(MonthTimeClient.get_stime_value_for_user_current_month(user_id) / 3600) # in hours
        study_streak = StreakClient.get_highest_study_streak_for_user(user_id)
        trivia = UserClient.get_user_trivia(user_id)

        rb_user = RbClient.get_rogue_boss_user(user_id)
        if rb_user is None or rb_user.status_code == 404:
            rb_xp = 0
        else:
            rb_xp = json.loads(rb_user.text)['xp']
        
        # Create list of currently owned achievements
        achievements_on_database = AchievementClient.get_achievements_for_user_content(user_id)
        earned_status = [i in achievements_on_database for i in range(len(achievements))]

        # ============================
        # Check all focus achievements
        # ============================
        for achievement in all_focus_achievements:
            if not earned_status[achievement['id']] and all_focus_time > achievement['value']:
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {user_id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        # ============================
        # Check month focus achievements
        # ============================
        for achievement in month_focus_achievements:
            if not earned_status[achievement['id']] and month_focus_time > achievement['value']:
                # Logic for month focus achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {user_id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        # ============================
        # Check study streak focus achievements
        # ============================
        for achievement in study_streak_achievements:
            if not earned_status[achievement['id']] and study_streak >= achievement['value']:
                # Logic for study streak achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {user_id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        # ============================
        # Check trivia achievements
        # ============================
        for achievement in trivia_achievements:
            if not earned_status[achievement['id']] and trivia >= achievement['value']:
                # Logic for trivia achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {user_id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        # ============================
        # Check rogue boss achievements
        # ============================
        for achievement in rb_level_achievements:
            if not earned_status[achievement['id']] and rb_xp >= achievement['value']:
                # Logic for rogue boss achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {user_id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        total_earned = earned_status.count(True)
        return total_earned, len(achievements)


    def get_achievements(self, interaction: discord.Interaction):
        '''
        Obtains the achievements for the user provided in interaction.user. We will display
        the achievements that correspond to where they are at in their AlderBot journey.

        For instance, there are 5 categories of achievements:
        1. all focus
        2. month focus
        3. study streak
        4. trivia
        5. rogue boss

        We will only display the achievement that the user has yet to achieve. For example,
        if the user has 1 total focus hour, they will see achievement[0] (the achievement
        for 10 total focus hours). If the user has 15 total focus hours, they are awarded
        achievement[0] (stored inside of the database), and if they called /achievements again,
        they would now see achievement[1] in the place of achievement[0], since they have
        surpassed the requirements to see the previous achievement.

        This will be the same for each achievement. Under the case that the user has all of
        the achievements in a specific category, it will display a full 'progress bar'
        associated to the final achievement in the category. (Having 5001 total focus hours
        will show a completed bar on achievement[6])
        
        This function will return the embed.
        '''
        # Ensure user is created on the database
        user_id = interaction.user.id
        UserClient.create_user_if_dne(user_id)

        # Retrieve data for achievements
        all_focus_time = math.floor(UserClient.get_user_stime(user_id) / 3600) # in hours
        month_focus_time = math.floor(MonthTimeClient.get_stime_value_for_user_current_month(user_id) / 3600) # in hours
        study_streak = StreakClient.get_highest_study_streak_for_user(user_id)
        trivia = UserClient.get_user_trivia(user_id)
        
        rb_user = RbClient.get_rogue_boss_user(user_id)
        if rb_user is None or rb_user.status_code == 404:
            rb_xp = 0
        else:
            rb_xp = json.loads(rb_user.text)['xp']
        
        # Create list of currently owned achievements
        achievements_on_database = AchievementClient.get_achievements_for_user_content(user_id)
        earned_status = [i in achievements_on_database for i in range(len(achievements))]

        # ============================
        # Check all focus achievements
        # ============================
        for achievement in all_focus_achievements:
            if not earned_status[achievement['id']] and all_focus_time > achievement['value']:
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {interaction.user.id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        first_unearned_index_all_focus = next((index for index, achievement in enumerate(all_focus_achievements) if not earned_status[achievement['id']]), None)

        # Check if all achievements have been earned, set the index to the last achievement if so
        if first_unearned_index_all_focus is None:
            first_unearned_index_all_focus = len(all_focus_achievements) - 1
        
        goal_all_focus_achievement = all_focus_achievements[first_unearned_index_all_focus]
        goal_all_focus_achievement_percent = round(all_focus_time / goal_all_focus_achievement['value'] * 100)
        if goal_all_focus_achievement_percent > 100: goal_all_focus_achievement_percent = 100
        Logger.debug(f'{user_id} Total focus achievement percent = {goal_all_focus_achievement_percent}%')

        # ============================
        # Check month focus achievements
        # ============================  
        for achievement in month_focus_achievements:
            if not earned_status[achievement['id']] and month_focus_time > achievement['value']:
                # Logic for month focus achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {interaction.user.id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        first_unearned_index_month_focus = next((index for index, achievement in enumerate(month_focus_achievements) if not earned_status[achievement['id']]), None)
        # Check if all achievements in month achievements have been earned, set the index to the last achievement if so
        if first_unearned_index_month_focus is None:
            first_unearned_index_month_focus = len(month_focus_achievements) - 1

        goal_month_focus_achievement = month_focus_achievements[first_unearned_index_month_focus]
        if earned_status[month_focus_achievements[5]['id']]:
            goal_month_focus_achievement_percent = 100
        else:
            goal_month_focus_achievement_percent = round(month_focus_time / goal_month_focus_achievement['value'] * 100)
        if goal_month_focus_achievement_percent > 100: goal_month_focus_achievement_percent = 100
        Logger.debug(f'{user_id} Month focus achievement percent = {goal_month_focus_achievement_percent}%')

        # ============================
        # Check study streak focus achievements
        # ============================
        for achievement in study_streak_achievements:
            if not earned_status[achievement['id']] and study_streak >= achievement['value']:
                # Logic for study streak achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {interaction.user.id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        first_unearned_index_study_streak = next((index for index, achievement in enumerate(study_streak_achievements) if not earned_status[achievement['id']]), None)
        # Check if all achievements in study streak achievements have been earned, set the index to the last achievement if so
        if first_unearned_index_study_streak is None:
            first_unearned_index_study_streak = len(study_streak_achievements) - 1

        goal_study_streak_achievement = study_streak_achievements[first_unearned_index_study_streak]
        goal_study_streak_achievement_percent = round(study_streak / goal_study_streak_achievement['value'] * 100)
        if goal_study_streak_achievement_percent > 100: goal_study_streak_achievement_percent = 100
        Logger.debug(f'{user_id} Study streak achievement percent = {goal_study_streak_achievement_percent}%')

        # ============================
        # Check trivia achievements
        # ============================
        for achievement in trivia_achievements:
            if not earned_status[achievement['id']] and trivia >= achievement['value']:
                # Logic for trivia achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {interaction.user.id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        first_unearned_index_trivia = next((index for index, achievement in enumerate(trivia_achievements) if not earned_status[achievement['id']]), None)
        # Check if all achievements in trivia achievements have been earned, set the index to the last achievement if so
        if first_unearned_index_trivia is None:
            first_unearned_index_trivia = len(trivia_achievements) - 1
        
        goal_trivia_achievement = trivia_achievements[first_unearned_index_trivia]
        goal_trivia_achievement_percent = round(trivia / goal_trivia_achievement['value'] * 100)
        if goal_trivia_achievement_percent > 100: goal_trivia_achievement_percent = 100
        Logger.debug(f'{user_id} trivia achievement percent = {goal_trivia_achievement_percent}%')

        # ============================
        # Check rogue boss achievements
        # ============================
        for achievement in rb_level_achievements:
            if not earned_status[achievement['id']] and rb_xp >= achievement['value']:
                # Logic for rogue boss achievements
                Logger.debug(f'Attempting to insert achievement {achievement["id"]} to {interaction.user.id}')
                AchievementClient.add_user_achievement_id(user_id, achievement['id'])
                earned_status[achievement['id']] = True

        first_unearned_index_rb = next((index for index, achievement in enumerate(rb_level_achievements) if not earned_status[achievement['id']]), None)
        # Check if all achievements in rb level achievements have been earned, set the index to the last achievement if so
        if first_unearned_index_rb is None:
            first_unearned_index_rb = len(rb_level_achievements) - 1
        
        goal_rb_level_achievement = rb_level_achievements[first_unearned_index_rb]
        goal_rb_level_achievement_percent = round(rb_xp / goal_rb_level_achievement['value'] * 100)
        if goal_rb_level_achievement_percent > 100: goal_rb_level_achievement_percent = 100
        Logger.debug(f'{user_id} rb level achievement percent = {goal_rb_level_achievement_percent}%')

        # ======================
        # Generate discord embed
        # ======================
        total_earned = earned_status.count(True)

        # Fetch the caller's hex code
        hex_string = UserClient.get_user_hex(user_id)
        hex_integer = int(hex_string, 16)

        red = (hex_integer >> 16) & 0xff
        green = (hex_integer >> 8) & 0xff
        blue = hex_integer & 0xff

        color = discord.Colour.from_rgb(red, green, blue)

        embed = discord.Embed(title=f'**{interaction.user.name}**\'s Narlock Achievements', description=f'Earned **{total_earned}/{len(achievements)}**', color=color)
        try:
            embed.set_thumbnail(url=f'{interaction.user.avatar.url}')
        except Exception as e:
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        
        embed.add_field(name=f'🔍 {goal_all_focus_achievement["title"]}', value=f'*{goal_all_focus_achievement["desc"]}*\n{self.get_progress_bar_by_percent(goal_all_focus_achievement_percent)}', inline=False)
        embed.add_field(name=f'📅 {goal_month_focus_achievement["title"]}', value=f'*{goal_month_focus_achievement["desc"]}*\n{self.get_progress_bar_by_percent(goal_month_focus_achievement_percent)}', inline=False)
        embed.add_field(name=f'🔥 {goal_study_streak_achievement["title"]}', value=f'*{goal_study_streak_achievement["desc"]}*\n{self.get_progress_bar_by_percent(goal_study_streak_achievement_percent)}', inline=False)
        embed.add_field(name=f'❓ {goal_trivia_achievement["title"]}', value=f'*{goal_trivia_achievement["desc"]}*\n{self.get_progress_bar_by_percent(goal_trivia_achievement_percent)}', inline=False)
        embed.add_field(name=f':crossed_swords: {goal_rb_level_achievement["title"]}', value=f'*{goal_rb_level_achievement["desc"]}*\n{self.get_progress_bar_by_percent(goal_rb_level_achievement_percent)}', inline=False)
        return embed
    