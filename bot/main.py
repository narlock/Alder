"""
Alder main.py
author: narlock

The main runner of the Alder.

The usage of "calling user" refers to the user that issues the command
on Discord.
"""

# Configuration dependency
import cfg

# Time for tracking how long an operation takes
import time

# Python dependencies
import re
import traceback
from datetime import datetime, timedelta, timezone

# API clients
from client.alder.interface.user_client import UserClient
from client.alder.interface.accomplishment_client import AccomplishmentClient
from client.alder.interface.rogueboss_client import RbClient
from client.alder.interface.dailytoken_client import DailyTokenClient

# Discord dependencies
import discord
from discord.ext import commands, tasks

# Tool dependencies
from tools.log import Logger
from tools.roleassign import RoleAssign
from tools.resetmonth import ResetMonth

# Time tracking application dependencies
from apps.time.time_track import TimeTrack
from apps.time.top import Top

# Shop application dependencies
from apps.shop.shop import Shop
from apps.shop.shopembed import ShopEmbed
from apps.shop.shopcolor import ShopColor

# Miscellaneous application dependencies
from apps.misc.roles import RolesToggleButton
from apps.misc.eight_ball import EightBall
from apps.misc.roll import Roll
from apps.misc.motivation import Motivation

# Bot information application dependencies
from apps.info.help import Help
from apps.info.help import HelpPageTurner
from apps.info.rules import Rules
from apps.info.stats import Stats
from apps.info.achievement import Achievements

# Arcade application dependencies
from apps.arcade.trivia import Trivia
from apps.arcade.trivia import TriviaButtons
from apps.arcade.rb import RogueBoss
from apps.arcade.rb import RogueBossTypeChooser

# Productivity application dependencies
from apps.productivity.todo import Todo
from apps.productivity.kanban import Kanban
from apps.productivity.deep_focus import DeepFocus

"""
Initialize AlderBot and required connections.

This creates the Bot object, specifies permitted servers,
establishes MySQL database connection, and defines
application connections.
"""
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
installed_server_id = cfg.DISCORD_SERVER_ID
Logger.info(f"Bot {bot}, serverId {installed_server_id}")

"""
Initialize the different dependencies
requires for the bot to perform
its defined operations
"""

# Profile
achievements_interface = Achievements()
profile_interface = Stats(achievements_interface)

# Tools
role_assign = RoleAssign()
reset_month = ResetMonth()

# # Time tracking
time_tracker = TimeTrack()
top_app = Top()

# # Shop
shopembed_app = ShopEmbed()
shopcolor_app = ShopColor()

# # Productivity
todo_app = Todo()
kanban_app = Kanban()
deepfocus_app = DeepFocus()

# # Arcade
trivia_app = Trivia()
rogue_boss = RogueBoss()

##########################################
##########################################
# Initialization and change events
##########################################
##########################################

@bot.event
async def on_ready():
    """
    The on_ready event will trigger when the bot starts up

    1. Ensures that the AlderBot is only connected to allowed servers.
    2. Begins to track member focus time
    3. Sets the status of the AlderBot.
    4. Syncs the slash commands.
    5. Refreshes button role interface in role channel.

    The bot will log a success message when this process is complete.
    """
    Logger.info(f'The current month is {stored_utc_month}')
    start_time = time.perf_counter()  # Start timing

    # bot is only allowed on allowed servers
    Logger.success(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        if guild.id != installed_server_id:
            Logger.info(f'{bot.user} leaving unauthorized server {guild.name} (id: {guild.id})')
            await guild.leave()
        else:
            Logger.info(f'{bot.user} is connected to {guild.name} (id: {guild.id})')
            # Begin to track active members in dedicated focus rooms
            time_tracker.start_up(guild)

    # Set status message
    await bot.change_presence(activity=discord.Game(name="/help • @narlockdev"))

    # Sync commands
    synced = await bot.tree.sync()
    Logger.info('AlderBot Slash Commands Synced: ' + str(len(synced)))

    channel = bot.get_channel(cfg.ROLE_CHANNEL_ID)
    if channel:
        # Delete the previous message if it exists
        async for message in channel.history(limit=1):
            await message.delete()

        # Send a new message
        await channel.send(cfg.ROLES_MESSAGE, view=RolesToggleButton())

    # Begin scheduled tasks
    sync_time_track.start()

    # Indicate on_ready is complete
    Logger.success('AlderBot is officially ready for use!')
    # End and log execution time for the command
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    Logger.info(f"Alder on_ready executed in {elapsed_time:.1f} seconds")

@bot.event
async def on_guild_join(guild):
    """
    The on_guild_join functionality is used to ensure that the AlderBot
    only joins servers that is has been assigned to join.

    AlderBot will leave servers that it has not been assigned to join.
    """
    guild_id = guild.id
    Logger.info(f"Joined guild with ID: {guild_id}")

    if guild.id != installed_server_id:
        await guild.leave()
        Logger.info(f"Bot removed from unauthorized server: {guild.name}")
    else:
        Logger.info(f"Bot joined authorized server: {guild.name}")

##########################################
##########################################
# Scheduled events
##########################################
##########################################
# stored_utc_month = datetime.now(timezone.utc).month
stored_utc_month = datetime.now(timezone.utc).month
stored_utc_year = datetime.now(timezone.utc).year

@tasks.loop(minutes=15)
async def sync_time_track():
    Logger.info('Syncing time track and checking for next month...')
    global stored_utc_month # Make global
    global stored_utc_year
    
    # Retrieve server
    guild = bot.get_guild(cfg.DISCORD_SERVER_ID)
    if guild:
        Logger.debug(f'Found discord server with id {cfg.DISCORD_SERVER_ID}')

        # Sync time track
        time_tracker.update_connected_users(guild)

        # Check for month reset
        current_utc_month = datetime.now(timezone.utc).month
        current_utc_year = datetime.now(timezone.utc).year
        if(stored_utc_month != current_utc_month):
            # If the stored month is not the current month, perform reset           
            Logger.debug(f'Performing month reset...') 
            await reset_month.reset_month(guild, stored_utc_month, stored_utc_year)

            # Store new values
            stored_utc_month = current_utc_month
            stored_utc_year = current_utc_year
        else:
            Logger.debug('The stored month is the same as the current month.')
    else:
        Logger.warn('The server was not found in config. Unable to sync time and month information')

##########################################
##########################################
# Discord staff commands
# Commands only accessible to those with
# specific server entitlements
##########################################
##########################################

@bot.command(name='shutdown')
async def shutdown(ctx: commands.Context):
    """
    $shutdown

    A traditional context command for administrator use only.
    This will shut the bot down at any given time.
    This command acts as a 'safe' shut down. This means that
    the current users inside of assigned focus rooms will
    keep the time that they focused for before the bot completes
    the shutdown process.

    Utilizes apps/time/time_track.py to save time information before
    shutting down
    """
    Logger.info(f"Received shutdown command from {ctx.author.name}")
    guild = ctx.guild
    user_has_role = discord.utils.get(ctx.author.roles, id=cfg.ADMIN_ROLE_ID) is not None
    if user_has_role:
        # Save the time and tokens earned for each connected user
        time_tracker.handle_shutdown(guild)

        # Alert server of shut down
        await ctx.send("Alder is powering off...")

        # Shut down bot
        await bot.close()
        Logger.success(f"AlderBot Closed Successful")
    else:
        await ctx.send("LOL! :rofl:")
        Logger.warn(f"Shutdown attempt failure. User {ctx.author.name} has insufficient permissions.")

@bot.command(name='givetokens')
async def give_tokens(ctx: commands.Context, user_id: int, num_tokens: int):
    """
    $givetokens {user_id} {num_tokens}

    A traditional context command for administrator use only.
    Adds {num_tokens} tokens to the Discord user with the id
    from {user_id}.
    """
    Logger.debug(f"Received givetokens command from {ctx.author.name}")
    user_has_role = discord.utils.get(ctx.author.roles, id=cfg.ADMIN_ROLE_ID) is not None
    if user_has_role:
        # Ensure that the user receiving tokens has a profile
        UserClient.create_user_if_dne(user_id)

        # Give tokens to user with user_id
        UserClient.add_tokens_user(user_id, num_tokens)

        # Send response message
        await ctx.send(f'{num_tokens} given to {user_id}')
        Logger.success(f"{ctx.author.name} successfully gave {num_tokens} tokens to {user_id}")
    else:
        # User has insufficient permissions to give tokens
        await ctx.send("LOL! :rofl:")
        Logger.warn(f"Give tokens failure. User {ctx.author.name} has insufficient permissions.")

@bot.command(name='giveacc')
async def give_accomplishment(ctx: commands.Context, user_id: int, message: str):
    """
    $giveacc {user_id} {message}

    A traditional context command for administrator use only.
    Adds accomplishment with the message passed in the {message}
    parameter to the user with the id {user_id}. Data is
    persisted through MySQLConnection.
    """
    Logger.info(f'Received give_accomplishment command from {ctx.author.name}')
    user_has_role = discord.utils.get(ctx.author.roles, id=cfg.ADMIN_ROLE_ID) is not None
    if user_has_role:
        AccomplishmentClient.add_user_accomplishment(user_id, message)
        await ctx.send(f'New accomplishment given to {user_id}')
        Logger.success(f"Successfully gave accomplishment {message} to {user_id}")
    else:
        await ctx.send("LOL! :rofl:")
        Logger.warn(f"Give accomplishment failure. User {ctx.author.name} has insufficient permissions.")

@bot.command(name='resetmonth')
async def resetmonth(ctx: commands.Context):
    """
    $resetmonth

    Traditional context command for administrator use only.
    This will reset the monthly roles for the users.

    Utilizes tools/resetmonth.py to handle resetting month
    """
    Logger.info(f"Received resetmonth command from {ctx.author.name}")
    user_has_role = discord.utils.get(ctx.author.roles, id=cfg.ADMIN_ROLE_ID) is not None
    if user_has_role:
        await reset_month.reset_month(ctx)
        Logger.success(f"AlderBot Reset Month Successful")
    else:
        await ctx.send("LOL! :rofl:")
        Logger.warn(f"Reset Month attempt failure. User {ctx.author.name} has insufficient permissions.")

##########################################
##########################################
# Voice Events
##########################################
##########################################

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """
    The on voice state update function will compare the before and after voice state
    of the user. Given this information, the TimeTracker will determine the amount of
    time earned and tokens earned. After this is updated, RoleAssign will check
    if any activity roles need to be assigned.

    Utilizes apps/time/time_track.py to handle activity updates
    """
    Logger.info(f"Handling voice state update for {member.name}")
    guild = member.guild

    time_tracker.update_time_on_event(member, before, after)
    await role_assign.check_role_updates_on_user(member, guild)

##########################################
##########################################
# Profile Commands
##########################################
##########################################

@bot.tree.command(name='stats', description='(deprecated) Displays profile statistics')
async def stats(interaction: discord.Interaction, member: discord.Member = None):
    """
    See `profile` function.
    Deprecated in favor of using the `profile` command naming.
    """
    await handle_profile_stats(interaction, member)

@bot.tree.command(name='profile', description='Displays profile statistics')
async def profile(interaction: discord.Interaction, member: discord.Member = None):
    """
    /profile {optional: member}

    Displays the AlderBot profile statistics of the specified Discord member. If no member is
    provided, the calling user is set as the member.
    """
    await handle_profile_stats(interaction, member)

async def handle_profile_stats(interaction: discord.Interaction, member: discord.Member = None):
    """
    Handles the logic of a profile or stats command.

    Utilizes:
    - apps/time/time_track.py to handle time statistics
    - apps/info/achievement.py to handle achievements
    - tools/roleassign.py to handle activity roles
    - apps/info/stats.py to handle displaying statistics embed
    """
    start_time = time.perf_counter()  # Start timing

    try:
        Logger.info(f"Profile stats command received from {interaction.user.name} with member = {member}")
        
        # Set the member to the calling user if none is provided
        if member is None:
            member = interaction.guild.get_member(interaction.user.id)

        # Ensure that statistics for the member are updated
        time_tracker.update_time_on_call(interaction, member)
        guild = interaction.guild

        # Ensure that achievements are earned if applicable for member
        achievements_interface.get_achievements(interaction)

        # Check if the member has earned a higher activity role
        await role_assign.check_role_updates_on_user(member, guild)

        # Create discord embed from profile information
        embed = profile_interface.create_profile_embed(interaction, member)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        traceback.print_exc()
        Logger.error(f"Error obtaining member {member} and guild from incoming interaction. {e}")
        await interaction.response.send_message(embed=cfg.NO_PROFILE_EMBED)

    # End and log execution time for the command
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    Logger.info(f"Profile stats command executed in {elapsed_time:.1f} seconds")

@bot.tree.command(name='achievements', description='View achievement progress')
async def achievements(interaction: discord.Interaction):
    """
    /achievements

    Displays the achievement progress of the calling user. This function will
    also refresh the achievement context for the calling user.

    Utilizes apps/info/achievement.py to accomplish achievement functions.
    """
    Logger.info(f'Achievements command received from {interaction.user.name}')
    try:
        Logger.debug(f'Attempting to get member achievements for {interaction.user.name}')
        embed = achievements_interface.get_achievements(interaction)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        traceback.print_exc()
        Logger.error(f"Error obtaining member and guild from incoming interaction. {e}")
        await interaction.response.send_message(embed=cfg.ErrorEmbed.message("Unexpected error occurred when retrieiving achievements"))

@bot.tree.command(name='top', description='View server leaderboards')
async def top(interaction: discord.Interaction, board: str = None):
    """
    /top {optional: board}

    Displays the top leaderboard users based on the {board} parameter.
    If no board is provided to this function, the monthly focus time
    leaderboard will be returned.

    Utilizes apps/time/top.py to handle leaderboard information.
    """
    Logger.info(f"Top command received from {interaction.user.name} where board is {board}")
    
    # Leaderboards that are available
    board_options = {
        None: top_app.display_top,
        'trivia': top_app.display_top_trivia,
        'rb': top_app.display_top_rb,
        'all': top_app.display_top_all,
        'streak': top_app.display_top_streak,
        'hstreak': top_app.display_top_streaks_all_time,
        'daily': top_app.display_top_daily
    }

    # Get the corresponding function from the dictionary or return an error message
    embed = board_options.get(board, lambda _: cfg.ErrorEmbed.message(
        'Invalid parameter: board.\nOptions: `daily`, `all`, `trivia`, `rb`, `streak`, `hstreak`'))(interaction)

    # Send the embed in response to the interaction
    await interaction.response.send_message(embed=embed)

# ##########################################
# ##########################################
# # Shop Commands
# ##########################################
# ##########################################

@bot.tree.command(name='shop', description='View the shop listings.')
async def shop(interaction: discord.Interaction):
    """
    /shop

    Displays the current server shop options.

    Utilizes apps/shop/shop.py to display shop options
    """
    Logger.info(f"Shop command received from {interaction.user.name}")
    embed = Shop.show_shop_options()
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='shopembed', description='Use 1000 tokens to change the color of your profile embed.')
async def shopembed(interaction: discord.Interaction, hex: str = None):
    """
    /shopembed {hex}

    Given a hex value representing a color, this function will
    handle the operation of either giving setting the color to
    the calling user's profile embed. If a hex value does not
    match the required regular expression (`FFFFFF` for example,
    is the color white) then the application will ask the user
    to provide a correctly formatted hex color for AlderBot to
    understand.

    Utilizes apps/shop/shopembed.py to handle shopembed interaction.
    """
    Logger.info(f"Shop Embed command received from {interaction.user.name}")

    # Ensures that the user has earned their tokens
    time_tracker.update_time_on_call(interaction, interaction.user)
    
    # Determines purchase result
    if hex and re.match(r'^[0-9a-fA-F]{6}$', hex):
        embed = shopembed_app.purchase_embed(interaction.user.id, hex)
    else:
        embed = cfg.ErrorEmbed.message(f"{interaction.user.mention}, please provide a correct hex code. Example: `FFFFFF` is white in hex. To send command with this hex, you would use `/shopembed FFFFFF`")

    # Send the embed in response to the interaction
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name='shopcolor', description='Use 500 tokens to change the color of your discord name!')
async def shopcolor(interaction: discord.Interaction, color: str = None):
    """
    /shopcolor {optional: color}
    
    With no passed {color} parameter. The choices of colors will be
    presented to the calling user. By passing an {color} parameter,
    a purchase on the color role associated with {color} will be
    initiated by the shopcolor_app.

    Utilizes:
    - apps/time/time_track.py for ensuring tokens have been given
    - apps/shop/shopcolor.py for handling shopcolor interaction.
    """
    Logger.info(f"Shopcolor command received by {interaction.user.name} where color = {color}")
    
    # Ensures that the user has earned their tokens
    time_tracker.update_time_on_call(interaction, interaction.user)

    if color is None:
        # Present available colors as interaction response
        embed = shopcolor_app.show_color_shop()
        await interaction.response.send_message(embed=embed)
    else:
        try:
            # Attempt to parse color option
            purchase_number = int(color)

            # Validate parsed color option
            if purchase_number >= 1 and purchase_number <= 16:
                # Handle purchase
                embed = await shopcolor_app.purchase_color(interaction.user, interaction.guild, purchase_number)
                await interaction.response.send_message(embed=embed)
            else:
                # Handle invalid color option (although the parse was successful)
                Logger.error(f'Unable to process shopcolor command from {interaction.user.name}. Color parameter {color} is not between 1 and 16.')
                embed = cfg.INVALID_COLOR_EMBED
                await interaction.response.send_message(embed=embed)
        except Exception:
            # Handle invalid color option (unable to parse color)
            Logger.error(f'Unable to process shopcolor command from {interaction.user.name}. Color parameter {color} failed to be parsed to an integer.')
            embed = cfg.INVALID_COLOR_EMBED
            await interaction.response.send_message(embed=embed)

# ##########################################
# ##########################################
# # Misc Commands
# ##########################################
# ##########################################

@bot.tree.command(name='roll', description='Rolls a random number between 1 and a max number (default 100)')
async def roll(interaction: discord.Interaction, max_roll: str = '100'):
    """
    /roll {optional: max_roll}

    If no {max_roll} is provided, roll will roll a random number between 
    1 and 100. If a {max_roll} parameter is provided, roll will roll a
    random number between 1 and {max_roll}

    Utilizes /apps/misc/roll.py for roll logic and response embed.
    """
    Logger.info(f"Roll command received from {interaction.user.name}")
    embed = Roll.perform_action(interaction, max_roll)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='8ball', description='Magic 8 ball')
async def eightball(interaction: discord.Interaction, question: str):
    """
    /8ball {question}

    User can ask a {question} and receive a random response, similar to a magic 8-ball.

    Utilizes /apps/misc/8ball.py for 8ball logic and response embed
    """
    Logger.info(f"8Ball command received from {interaction.user.name}")
    response = EightBall.get_response()
    await interaction.response.send_message(f'**Question**: {question}\n**Answer**: {response}')

@bot.tree.command(name='motivation', description='Get some motivation!')
async def motivation(interaction: discord.Interaction, user: discord.User = None):
    """
    /motivation {optional: user}

    The motivation command will send motivation to the calling user. If
    a user is passed to the {user} parameter, the calling user will be
    giving motivation to the user passed in the parameter.

    Utilizes /apps/misc/motivation.py to create a motivation message for the user.
    """
    Logger.info(f"Motivation command received from {interaction.user.name}")
    response = Motivation.get_motivation_embed(interaction, user)
    await interaction.response.send_message(response)

# ##########################################
# ##########################################
# # Information Commands
# ##########################################
# ##########################################

@bot.tree.command(name='help', description='Information on how to use AlderBot')
async def help(interaction: discord.Interaction):
    """
    /help

    Displays an interactive embed containing documentation for using
    the AlderBot functions as a user.

    Utilizes /apps/info/help.py for embed integration
    """
    Logger.info(f"Help command received from {interaction.user.name}")
    embed = Help.get_help_embed()
    await interaction.response.send_message(embed=embed, view=HelpPageTurner(embed, interaction.user.id), ephemeral=True)

@bot.tree.command(name='rules', description='Displays the rules for the server.')
async def rules(interaction: discord.Interaction):
    """
    /rules

    Displays the rules for the server.

    Utilizes /apps/info/rules.py to create embed for rules.
    """
    Logger.info(f"Rules command received from {interaction.user.name} in {interaction.guild.name}")
    
    # Retrieve the rules channel for embed
    rules_channel = bot.get_channel(cfg.RULES_CHANNEL_ID)

    # Construct rules embed and return as interaction response
    embed = Rules.get_rules_embed(rules_channel)
    await interaction.response.send_message(embed=embed)

# ##########################################
# ##########################################
# # Arcade Commands
# ##########################################
# ##########################################

@bot.tree.command(name='trivia', description='Answer fun trivia questions (25 tokens to play)')
async def trivia(interaction: discord.Interaction):
    """
    /trivia

    The calling user can play a game of trivia for 25 tokens.
    This function will determine if the user is eligible to play by
    checking how many tokens they own. If they have enough to play,
    an interactive embed will be returned that provides an interface
    to play. 25 tokens will also be subtracted from their total
    amount. If the calling user does not have enough tokens to play,
    they will receive an error message stating so.

    Utilizes apps/arcade/trivia.py to provide trivia game interface
    """
    Logger.info(f"Trivia command received from {interaction.user.name}")

    # Retrieve amount of tokens for calling user
    user_tokens = UserClient.get_user_tokens(interaction.user.id)

    if user_tokens < 25:
        # User cannot play trivia - not enough tokens
        embed = cfg.ErrorEmbed.notokens(user_tokens, 25)
        await interaction.response.send_message(embed=embed)
    else:
        # User can play - subtract tokens for playing
        UserClient.subtract_tokens_user(interaction.user.id, 25)

        # Return interactive embed for playing trivia
        embed = trivia_app.play_trivia(interaction)
        await interaction.response.send_message(embed=embed, view=TriviaButtons(embed, interaction.user.id))

@bot.tree.command(name='rb', description='Play Rogue Boss (25 tokens to play - active during study streams)')
async def rb(interaction: discord.Interaction, command: str = None):
    """
    /rb {optional: command}

    Rogue Boss (https://github.com/narlock/RogueBoss) is an interactive boss battle
    application. This command provides a front end interface for interacting and playing
    Rogue Boss.

    By not passing a {command} parameter. The calling user will be queried in the backend
    database for a Rogue Boss profile. If a profile exists, the calling user will be using an attack
    against the current Rogue Boss. If a profile does not exist, this function assumes that it
    is the initial setup for the calling user and will return an interactive embed and give
    an introduction to Rogue Boss.

    If "stats" is provided as the {command} parameter, the calling user will be queried in
    the backend database. If they are found, their Rogue Boss profile information will be displayed.
    If "type" is provided as the {command} parameter, the calling user will receive an
    information message containing type match ups in Rogue Boss.
    If any other input is given to this command, information for Rogue Boss will be presented unless
    the calling user does not have a profile for Rogue Boss.

    Utilizes apps/arcade/rb.py for interacting with Rogue Boss.
    """
    Logger.info(f'Received rb command from {interaction.user.name} with command {command}')
    user = RbClient.get_rogue_boss_user_content(interaction.user.id)

    if command is None:
        if user is None:
            # Allow the user to select their type - initial play - does not cost tokens
            embed = rogue_boss.initial()
            await interaction.response.send_message(embed=embed, view=RogueBossTypeChooser(embed, interaction.user.id))
        else:
            # Play Rogue Boss
            embed = rogue_boss.play_rb(interaction, user)
            await interaction.response.send_message(embed=embed)
    else:
        if user is None:
            embed = cfg.ErrorEmbed.message(f'User not initialized!\nTry </rb:{cfg.ROGUE_BOSS_COMMAND_ID}> to initialize!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if command == 'stats':
                embed = rogue_boss.show_stats(interaction, user)
                await interaction.response.send_message(embed=embed)
            elif command == 'type':
                embed = rogue_boss.show_type()
                await interaction.response.send_message(embed=embed)
            elif command.startswith('model'):
                # Grab index from second parameter
                split_command = command.split(' ', maxsplit=1)
                print(split_command[1])
                try:
                    index = int(split_command[1])
                    if index not in [0, 1]:
                        await interaction.response.send_message(embed=cfg.ErrorEmbed.message('Valid models are `0` and `1`.'))
                    else:
                        RbClient.update_rogue_boss_user_model(user['user_id'], index)
                        await interaction.response.send_message(f'Rogue Boss model changed to `{index}`')
                except:
                    await interaction.response.send_message(embed=cfg.ErrorEmbed.message('Expected integer value as index.'))
            else:
                # Display Rogue Boss information
                embed = rogue_boss.show_info()
                await interaction.response.send_message(embed=embed)

# ##########################################
# ##########################################
# # Productivity Commands
# ##########################################
# ##########################################

@bot.tree.command(name='deepfocus', description='Toggle deep focus mode')
async def deepfocus(interaction: discord.Interaction):
    """
    /deepfocus

    Toggles the deep focus role for the calling user. Displays the response
    message only to the calling user.

    Utilizes apps/productivity/deep_focus.py to handle deep focus
    """
    Logger.info(f"Toggling deep focus for {interaction.user.name}")
    await deepfocus_app.toggle_deep_focus(interaction)
    await interaction.response.send_message("Deep focus toggled - review your roles to validate!", ephemeral=True)

@bot.tree.command(name='todo', description='Todo list')
async def todo(interaction: discord.Interaction, command: str = None):
    """
    /todo {optional: command}

    Todo is a simple todo list interface that provides a simple todo list to
    the calling user. 
    
    Users can create a todo list item by simply providing
    the name of the item they want to complete as the {command} parameter.
    Ex: `/todo Something I need to get done` will create a todo list
    item with the title "Something I need to get done". It will be
    assigned an index number 1-10.

    Users can complete a todo list item by providing the index as
    the {command} parameter. 
    Ex: `/todo 1` will complete the todo list item in the first index.

    Users can update the contents of a todo list item by providing the
    index followed by a name for what they want to change the todo list
    item to.
    Ex: `/todo 1 Something else I need to do` will change the name of
    the first todo item to "Something else I need to do"

    Users can delete a specific todo item by passing "remove" followed
    by the index value of the todo list item they would like to remove.
    Ex: `/todo remove 1` will remove the todo list item in index 1.

    Users can delete all of their todo list items by providing "clear"
    as the {command} parameter.

    If no value is passed to the {command} parameter, the calling user's
    todo list will be returned as an embed.

    Utilizes apps/productivity/todo.py to provide todo list interface
    """
    Logger.info(f'Todo command received from {interaction.user.name} with command {command}')

    # Dictionary of options {command, function_value}
    todo_commands = {
        'clear': lambda: todo_app.clear_items(interaction),
        '1': lambda: todo_app.check_item(interaction, 1),
        '2': lambda: todo_app.check_item(interaction, 2),
        '3': lambda: todo_app.check_item(interaction, 3),
        '4': lambda: todo_app.check_item(interaction, 4),
        '5': lambda: todo_app.check_item(interaction, 5),
        '6': lambda: todo_app.check_item(interaction, 6),
        '7': lambda: todo_app.check_item(interaction, 7),
        '8': lambda: todo_app.check_item(interaction, 8),
        '9': lambda: todo_app.check_item(interaction, 9),
        '10': lambda: todo_app.check_item(interaction, 10)
    }

    if command is None:
        # Return the calling user's todo list
        embed = todo_app.get_todo_list(interaction)
        await interaction.response.send_message(embed=embed)
    else:
        # Some command whose response will only be shown to calling user
        command_lower = command.lower()
        handler = todo_commands.get(command_lower)

        if handler:
            # Handle input from todo_commands
            embed = handler()
        elif command_lower.startswith(('1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ')) and len(command_lower) > 3:
            # Handle updating a todo list item
            if command_lower[:2] == '10':
                index = 10
            else:
                index = int(command_lower[0])
            update_item_name = command[2:]
            embed = todo_app.update_item(interaction, index, update_item_name)
        elif command_lower.startswith('remove'):
            # Handle remove todo item
            index_str = command_lower[7:]
            if index_str.isdigit() and 1 <= int(index_str) <= 10:
                index = int(index_str)
                embed = todo_app.remove_item(interaction, index)
            else:
                embed = cfg.ErrorEmbed.message(f'Invalid index provided to `remove` operation: {index_str}')
        else:
            # Add a new todo item with the command string
            embed = todo_app.add_item(interaction, command)

        # Return embed that only the calling user can view
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
@bot.tree.command(name='kanban', description='Kanban productivity board')
async def kanban(interaction: discord.Interaction, command: str=None):
    """
    /kanban {optional: command}

    An alternative to a todo list, the kanban board offers a kanban interface
    for tracking tasks by splitting them up into three columns: todo, doing, and done.
    This command provides a simple interface for users to manage a personal kanban board.

    For information on using this command and development, visit:
    https://www.youtube.com/watch?v=5zJUIAigLeA

    Utilizes apps/productivity/kanban.py for kanban interface
    """
    Logger.info(f'Kanban command received from {interaction.user.name} with command {command}')

    # Function to parse flags in a given text
    def parse_flags(text, flag, delimiter=' '):
        flag_values = []
        if flag in text:
            flag_parts = text.split(flag)
            for part in flag_parts[1:]:
                part = part.strip()
                if delimiter in part:
                    flag_values.append(part.split(delimiter, 1)[0])
                else:
                    flag_values.append(part)
        return flag_values

    # View kanban board - Branch for /kanban
    if command is None:
        # /kanban action
        Logger.debug('Command was none for kanban. Returning kanban board.')
        embed = kanban_app.view_kanban_board(interaction)
        await interaction.response.send_message(embed=embed)

    # Move kanban item to next column - Branch for /kanban #
    elif command.isdigit():
        kanban_id = int(command)
        # /kanban # action with kanban_id
        Logger.debug('Command for Kanban was a digit. Attempting to move Kanban item to next column.')
        embed = kanban_app.move_kanban_item(interaction, kanban_id)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Branch for /kanban # {some_other_text}
    elif ' ' in command and command.split(' ', 1)[0].isdigit():
        parts = command.split(' ', 1)
        if parts[0].isdigit():
            kanban_id = int(parts[0])
            remaining_text = parts[1].strip()
            # check for column name
            if remaining_text.lower() in ['todo', 'doing', 'done']:
                column = remaining_text.lower()
                # /kanban # {column_name} action with kanban_id, column_name
                Logger.debug('Command was a digit with text. Attempting to move Kanban item to a specific column')
                embed = kanban_app.move_kanban_item_to_column(interaction, kanban_id, column)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                # Check for flags in some_other_string
                flags = ['-p', '-t', '-v']
                values = {flag: None for flag in flags}

                # Separate flags from the string part
                for flag in flags:
                    if flag in remaining_text:
                        flag_values = parse_flags(remaining_text, flag)
                        if flag == '-p':
                            Logger.debug('Priority flag found. Adding to flag values')
                            values[flag] = int(flag_values[0]) if flag_values else None
                        elif flag == '-v':
                            Logger.debug('Velocity flag found. Adding to flag values')
                            values[flag] = int(flag_values[0]) if flag_values else None
                        elif flag == '-t':
                            Logger.debug('Tag flag found. Adding to flag values')
                            values[flag] = flag_values

                # Extract the remaining string after removing flags
                remaining_string = remaining_text
                for flag in flags:
                    remaining_string = remaining_string.replace(f'{flag} {values[flag]}', '').strip()

                # Find the index of the first flag occurrence
                first_flag_index = min((remaining_text.find(flag) for flag in flags if flag in remaining_text), default=-1)

                # Extract the remaining string before the first flag
                if first_flag_index != -1:
                    some_other_string = remaining_text[:first_flag_index].strip()
                else:
                    some_other_string = remaining_text.strip()

                priority = values['-p']
                tag = values['-t'][0] if values['-t'] else None
                velocity = values['-v']

                # /kanban {some_other_string} action with some_other_string, priority, tag, velocity
                Logger.debug('Command initiated for updating kanban item.')
                embed = kanban_app.update_kanban_item(interaction, kanban_id, some_other_string, priority, tag, velocity)
                await interaction.response.send_message(embed=embed, ephemeral=True)

    # Branch for /kanban remove #
    elif command.startswith('remove ') and command[7:].isdigit():
        kanban_id = int(command[7:])
        # /kanban remove # action with kanban_id
        Logger.debug('Command was remove. Removing kanban item.')
        embed = kanban_app.remove_kanban_item(interaction, kanban_id)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    elif command.startswith('tag '):
        kanban_tag = command[4:]
        Logger.debug('Command starts with tag. Displaying the matching tag.')
        embed = kanban_app.view_kanban_board_tag(interaction, kanban_tag)
        await interaction.response.send_message(embed=embed)

    elif command == 'complete':
        embed = kanban_app.complete(interaction)
        Logger.debug('Command was complete. Removing Kanban items in done column.')
        await interaction.response.send_message(embed=embed)

    # Branch for /kanban {some_other_string}
    else:
        # Check for flags in some_other_string
        flags = ['-p', '-t', '-v']
        values = {flag: None for flag in flags}

        # Separate flags from the string part
        for flag in flags:
            if flag in command:
                flag_values = parse_flags(command, flag)
                if flag == '-p':
                    values[flag] = int(flag_values[0]) if flag_values else None
                elif flag == '-v':
                    values[flag] = int(flag_values[0]) if flag_values else None
                elif flag == '-t':
                    values[flag] = flag_values

        # Extract the remaining string after removing flags
        remaining_string = command
        for flag in flags:
            remaining_string = remaining_string.replace(f'{flag} {values[flag]}', '').strip()

        # Find the index of the first flag occurrence
        first_flag_index = min((command.find(flag) for flag in flags if flag in command), default=-1)

        # Extract the remaining string before the first flag
        if first_flag_index != -1:
            some_other_string = command[:first_flag_index].strip()
        else:
            some_other_string = command.strip()

        priority = values['-p']
        tag = values['-t'][0] if values['-t'] else None
        velocity = values['-v']

        # /kanban {some_other_string} action with some_other_string, priority, tag, velocity
        embed = kanban_app.add_kanban_item(interaction, some_other_string, priority, tag, velocity)
        Logger.debug('Adding the kanban item to user\'s board')
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ##########################################
# ##########################################
# # Sponsor commands
# # Commands only available to sponsors
# ##########################################
# ##########################################

@bot.tree.command(name='daily', description='Retrieve daily tokens!')
async def daily(interaction: discord.Interaction):
    """
    /daily

    Users that support the server (have the supporter, booster, etc.) roles can
    receive daily tokens as a thanks to their patronage.

    Gifts the calling user tokens based off of their supporting status.
    - Regular members receive no bonus and will be told that this is only for supporting members
    - Server boosters receive 25 tokens daily for supporting
    - Supporters receive 50 tokens daily for supporting

    The entire command functionality is provided from this function.
    """
    Logger.info(f'Daily tokens command received from {interaction.user.name}')
    booster_id = cfg.BOOSTER_ROLE_ID
    supporter_id = cfg.SUPPORTER_ROLE_ID
    role_ids_to_check = [booster_id, supporter_id]

    # Check if the user has either server booster or supporter
    user_roles = [role.id for role in interaction.user.roles]
    has_supporting_role = any(role_id in user_roles for role_id in role_ids_to_check)
    if has_supporting_role:
        # Retrieve daily token entry
        daily_token_date_time = DailyTokenClient.get_user_dailytoken_time_entry(interaction.user.id)

        if daily_token_date_time is None:
            # Under the case that the user has never used this command
            DailyTokenClient.set_dailytoken_entry_user_current_time(interaction.user.id, datetime.now())
            
            # Award tokens
            num_tokens = 0
            if booster_id in user_roles and supporter_id in user_roles:
                num_tokens = 75
            elif booster_id in user_roles:
                num_tokens = 25
            elif supporter_id in user_roles:
                num_tokens = 50

            if num_tokens > 0:
                UserClient.add_tokens_user(interaction.user.id, num_tokens)

                # Inform the user about the tokens received
                tokens_msg = f"You've received {num_tokens} tokens!"
                embed = discord.Embed(title='Alder Message', description=tokens_msg, color=discord.Color.green())
                embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
                embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
                await interaction.response.send_message(embed=embed)
        else:
            # Under the case where the user has redeemed tokens in the past
            current_time = datetime.now()
            time_difference = current_time - daily_token_date_time
            remaining_time = timedelta(hours=24) - time_difference

            if remaining_time.total_seconds() > 0:
                remaining_hours = int(remaining_time.total_seconds() // 3600)
                remaining_minutes = int((remaining_time.total_seconds() % 3600) // 60)
                remaining_time_str = f"{remaining_hours} hours and {remaining_minutes} minutes"

                # Construct your string with remaining time information
                remaining_msg = f"You need to wait {remaining_time_str} before obtaining more tokens."
                
                # Inform the user they have to wait before receiving more tokens from this command
                embed = discord.Embed(title=f'Alder Message', color=discord.Color.gold())
                embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
                embed.add_field(name='\u200b', value=f'{remaining_msg}')
                embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                DailyTokenClient.set_dailytoken_entry_user_current_time(interaction.user.id, datetime.now())

                # Award tokens
                num_tokens = 0
                if booster_id in user_roles and supporter_id in user_roles:
                    num_tokens = 75
                elif booster_id in user_roles:
                    num_tokens = 25
                elif supporter_id in user_roles:
                    num_tokens = 50

                if num_tokens > 0:
                    UserClient.add_tokens_user(interaction.user.id, num_tokens)
                    
                    # Inform the user about the tokens received
                    tokens_msg = f"You've received {num_tokens} tokens!"
                    embed = discord.Embed(title='Alder Message', description=tokens_msg, color=discord.Color.green())
                    embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
                    embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
                    await interaction.response.send_message(embed=embed)

    else:
        # If the calling user is not a supporter
        embed = discord.Embed(title=f'Alder Message', color=0xff0000)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='\u200b', value=f'Daily tokens are only available to **Server Boosters** and **Supporters**!\n→ To become a supporter, support on [Patreon](https://patreon.com/narlock)!', inline=False)
        embed.add_field(name='\u200b', value=f'**Boosters** can receive `25` tokens daily,\n**Supporters** can receive `50` tokens daily,\nand users with __both__ roles can receive `75` tokens daily!', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        await interaction.response.send_message(embed=embed)

# Starts AlderBot
bot.run(cfg.TOKEN)
