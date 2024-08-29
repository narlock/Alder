"""
time_track.py
author: narlock

Time track is an application interface for storing user activity time information.
It works by storing user focus time in the user_time dictionary. Where the key
will be the id of the Discord user, and the value will be the voice channel
join time. When the user disconnects from the voice channel or an application
function is called that requires the time to update, time and tokens will be
awarded to the user.
"""
import cfg
import discord
import time
import traceback

from tools.log import Logger
from client.alder.interface.user_client import UserClient
from client.alder.interface.dailytime_client import DailyTimeClient
from client.alder.interface.monthtime_client import MonthTimeClient
from client.alder.interface.streak_client import StreakClient

SECONDS_FOR_TOKEN = 300
ACTIVITY_ROOMS = cfg.ACTIVITY_CHANNEL_IDS
user_time = {}

class TimeTrack():
    def start_up(self, guild: discord.Guild):
        """
        Utilized when the bot starts up, this function will obtain
        the current voice channel information of the server and begin to
        count the focus time for the users that are currently connected to
        dedicated activity rooms.
        """
        try:
            voice_channels = guild.voice_channels
            Logger.debug(f"Obtained voice channels from guild {voice_channels}.")
        except Exception as e:
            Logger.error(f"An unexpected error occurred when fetching voice channels from guild. {e}")

        for channel in voice_channels:
            if isinstance(channel, discord.VoiceChannel) and channel.id in ACTIVITY_ROOMS:
                # Obtain the members in each activity room and begin to track time
                members = channel.members
                for member in members:
                    Logger.info(f"{member.name} was in {channel.name} on bot startup. Starting time.")
                    
                    # Put user into user_time dictionary for time tracking
                    user_time[member.id] = time.time()

                    # Create the user if they do not exist
                    UserClient.create_user_if_dne(member.id)
                    
    def handle_shutdown(self, guild: discord.Guild):
        voice_channels = guild.voice_channels
        Logger.debug(f"Successfully obtained voice channels from guild {voice_channels}.")

        for channel in voice_channels:
            if isinstance(channel, discord.VoiceChannel) and channel.id in ACTIVITY_ROOMS:
                # Obtain the members that are currently in activity rooms
                members = channel.members
                for member in members:
                    # If those members exist in the user_time dictionary, update their time and tokens before shutting down
                    if member.id in user_time:
                        # Calculate activity time and tokens earned
                        focused_time_of_member = round(time.time() - user_time[member.id])
                        tokens_earned = (focused_time_of_member // SECONDS_FOR_TOKEN)

                        # Update the user time and tokens earned
                        self.update_user_time_and_tokens_entry_in_database(member.id, focused_time_of_member, tokens_earned)
                        Logger.success(f"Member {member.name} time saved {focused_time_of_member}, earned {tokens_earned} tokens.")

    def update_connected_users(self, guild: discord.Guild):
        voice_channels = guild.voice_channels
        Logger.debug(f"Successfully obtained voice channels from guild {voice_channels}.")

        for channel in voice_channels:
            if isinstance(channel, discord.VoiceChannel) and channel.id in ACTIVITY_ROOMS:
                members = channel.members
                for member in members:

                    # If the user is connected, they should be in user_time
                    if member.id in user_time:
                        focused_time_of_member = round(time.time() - user_time[member.id])

                        tokens_earned = focused_time_of_member // SECONDS_FOR_TOKEN

                        # Resetting time
                        user_time[member.id] = time.time()

                        self.update_user_time_and_tokens_entry_in_database(member.id, focused_time_of_member, tokens_earned)
                        Logger.success(f"Member {member.name} time saved {focused_time_of_member}, earned {tokens_earned} tokens.")

    def update_time_on_event(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        Logger.debug(f"Update Time Event Received in Time Track for {member.name}. Current user_time {user_time}")

        # Validate study streak
        StreakClient.set_streak_for_user(member.id)

        # Event when joining a focus room
        if member.id not in user_time and (before.channel is None or before.channel not in ACTIVITY_ROOMS) and (after.channel is not None and after.channel.id in ACTIVITY_ROOMS):
            """
            Store user_time entry matching <member_id, time> key value pair.
            If /stats is ran when user is inside of vc (dictionary entry exists for
            that member_id) then we want to recalculate focus time, update the dictionary,
            update database, and reset the current focus time in the room to 0.
            """
            Logger.info(f'{member.name} joined {after.channel.name}')
            user_time[member.id] = time.time()
            UserClient.create_user_if_dne(member.id)

        # Event when leaving a focus room
        if member.id in user_time and before.channel is not None and before.channel.id in ACTIVITY_ROOMS and (after.channel is None or after.channel.id not in ACTIVITY_ROOMS):
            """
            Calculate the focus time, update database, and then remove the member id from the
            user_time dictionary as they are no longer in a focus room.
            """
            try:
                focused_time_of_member = round(time.time() - user_time[member.id])
                tokens_earned = (focused_time_of_member // SECONDS_FOR_TOKEN)

                Logger.info(f"{member.name} left {before.channel.name}. {focused_time_of_member} seconds added to time, earning {tokens_earned} tokens.")
                del user_time[member.id]

                self.update_user_time_and_tokens_entry_in_database(member.id, focused_time_of_member, tokens_earned)
            except KeyError as e:
                Logger.error(f"KeyError occurred when accessing user_time. Invalid Key: {e.args[0]}")
            except Exception as e:
                traceback.print_exc()
                Logger.error(f"An unexpected error occurred inside of TimeTrack.update_time_on_event for {member.name}.")

    def update_time_on_call(self, interaction: discord.Interaction, user: discord.User):
        """
        Under the condition that the /stats command is called on a particular user
        (if no user is provided, the calling user a part of the interaction will be
        inferred), the time will update and tokens will be awarded.

        Additionally, if the user is connected to the voice channel, their
        time will be reset.
        """
        # Initially sets the user id as the caller id
        calling_user = interaction.user

        # If a member id is given (ex. /stats Firebal#0676), this id is set
        if user is not None:
            calling_user = user

        # Resiliency check: ensure the user exists in the database
        UserClient.create_user_if_dne(calling_user.id)

        # Check if user is in voice channel, if they are update info accordingly
        if calling_user.id in user_time:
            # Update Time based on voice connection
            try:
                focused_time_of_member = round(time.time() - user_time[calling_user.id])

                tokens_earned = focused_time_of_member // SECONDS_FOR_TOKEN

                # Resetting Time
                user_time[calling_user.id] = time.time()

                Logger.info(f"Updating profile statistics for {calling_user.id}. {focused_time_of_member} seconds added to time, earning {tokens_earned} tokens.")

                # Update MySQL User Entry
                self.update_user_time_and_tokens_entry_in_database(calling_user.id, focused_time_of_member, tokens_earned)
            except KeyError as e:
                Logger.error(f"KeyError occurred when accessing user_time. Invalid Key: {e.args[0]}")
            except:
                Logger.error(f"An unexpected error occurred inside of TimeTrack.update_time_on_event.")

    def update_user_time_and_tokens_entry_in_database(self, user_id, focus_time, tokens):
        # Resiliency check: ensure that the user has been created on the database
        UserClient.create_user_if_dne(user_id)

        # Update user resource
        UserClient.add_stime_and_tokens_user(user_id, focus_time, tokens)

        # Update dailytime resource
        DailyTimeClient.add_stime_to_user_dailytime(user_id, focus_time)

        # Update monthtime
        MonthTimeClient.add_stime_to_user_monthtime(user_id, focus_time)
