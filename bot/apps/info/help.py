"""
help.py
author: narlock

Interface for help with Alder operations.
"""

import cfg
import discord

GENERAL_HELP_VALUE = f'</help:{cfg.HELP_COMMAND_ID}> Get help! Oh wait, you\'re already here.\n</rules:{cfg.RULES_COMMAND_ID}> View the server rules.\n</profile:{cfg.PROFILE_COMMAND_ID}> View your profile.\n→ Using `/profile [member]` will display that member\'s profile!\n→ `/timezone` View and set your timezone.\n</achievements:{cfg.ACHIEVEMENTS_COMMAND_ID}> View your achievement progress.\n</roll:{cfg.ROLL_COMMAND_ID}> Randomly roll a number.\n</8ball:{cfg.EIGHTBALL_COMMAND_ID}> Ask the magic 8 ball a question.\n</motivation:{cfg.MOTIVATION_COMMAND_ID}> Get some motiviation!'

class HelpPageTurner(discord.ui.View):
    def __init__(self, embed: discord.Embed, user_id: int):
        super().__init__(timeout=None)
        self.embed = embed
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if the user who clicked the button is the same as the user who initiated the game."""
        return interaction.user.id == self.user_id
    
    @discord.ui.button(label='🛠️ General', style=discord.ButtonStyle.blurple)
    async def options_general(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='🛠️ **General**', value=GENERAL_HELP_VALUE, inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🗂️ Kanban', style=discord.ButtonStyle.blurple)
    async def options_kanban(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='🗂️ **Kanban**', value=f'</kanban:{cfg.KANBAN_COMMAND_ID}> View and share Kanban board.\n→`/kanban [task I need to do]` Add a task to do.\n:small_blue_diamond: Add optional flags to customize each task:\n:small_orange_diamond: Add `-p [1-3]` to add task priority. 🔵 🟡 🔴\n:small_orange_diamond: Add `-t [tagname]` to set a tag for your task. Tags must be a single word.\n:small_orange_diamond: Add `-v [#]` to set task velocity\n→`/kanban [#]` Move task to the next column.\n→`/kanban complete` Remove completed items\n→`/kanban tag [tagname]` View and share Kanban (tasks match tag)\n→`/kanban remove [#]` Removes a task.\n→`/kanban [#] [todo|doing|done]` Move task to column.\n→`/kanban [#] [task name -flags]` Overwrite task.', inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='📝 Todo', style=discord.ButtonStyle.blurple)
    async def options_todo(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='📝 **Todo**', value=f'</todo:{cfg.TODO_COMMAND_ID}> View and share your todo list.\n→ `/todo [task I need to complete]` to add a task to your todo list!\n→ `/todo [#]` to complete a selected task.\n→ `/todo [#] [My updated name for my task]` to update your task name.\n→ `/todo remove [#]` to remove a todo list item.\n→ `/todo clear` to clear your todo list.', inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='⏰ Reminders', style=discord.ButtonStyle.blurple)
    async def options_todo(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='⏰ **Reminders**', value=f'`/reminders` View your active reminders.\n→ `/reminders title: remind_date:YYYY-MM-DD remind_time:HH:MM` create a one time reminder!\n→ Add a `repeat_interval` of `daily`, `weekly`, or `monthly` to be reminded on interval!\n→ `/deletereminder [#]` to delete an active reminder.', inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🏆 Leaderboards', style=discord.ButtonStyle.blurple)
    async def option_leaderboards(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='🏆 **Leaderboards**', value=f'</top:{cfg.TOP_COMMAND_ID}> View Focus Leaders.\n→ `/top daily` - View Daily Focus Leaders.\n→ `/top all` - View All-Time Focus Leaders.\n→ `/top trivia` - View members with most trivia questions answered.\n→ `/top rb` View top Rogue Boss players.\n→ `/top streak` View top users by current streak.\n→ `/top hstreak` View top users by highest achieved streak.', inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🛍️ Shop', style=discord.ButtonStyle.blurple)
    async def option_shop(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='🛍️ **Shop**', value=f'</shop:{cfg.SHOP_COMMAND_ID}> View the shop listings\n</shopembed:{cfg.SHOP_EMBED_COMMAND_ID}> Change the color of your profile embed for `1000` :coin: tokens.\n→ Usage Example: `/shopembed FFFFFF` changes profile embed to white.\n</shopcolor:{cfg.SHOP_COLOR_COMMAND_ID}> Change your monthly server name color for `500` :coin: tokens.\n→ Use just `/shopcolor` to view the monthly colors!\n→Usage: `/shopcolor 1` will purchase the color associated to index 1.', inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🕹️ Arcade', style=discord.ButtonStyle.blurple)
    async def option_arcade(self, interaction: discord.Interaction, button: discord.ui.button):
        self.embed.set_field_at(0, name='🕹️ **Arcade**', value=f'</trivia:{cfg.TRIVIA_COMMAND_ID}> Answer fun and simple trivia questions.\n→ A single play costs `25` tokens.\n→ View trivia leaderboard with `/top trivia`\n</rb:{cfg.ROGUE_BOSS_COMMAND_ID}> Take on Boss battles during streams!\n→ Initally, member will choose their Rogue Boss type!\n→ After choosing a type, using `/rb` will attack the boss!\n→ Use `/rb info` to view additional commands.', inline=False)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='🌟 Supporters', style=discord.ButtonStyle.blurple)
    async def option_supporter(self, interaction: discord.Interaction, button:discord.ui.button):
        self.embed.set_field_at(0, name='🌟 **Supporters**', value=f'**Server Boosters** and **Supporters** gain access to exclusive commands on the server. If you are a booster or supporter, thank you so much for your contributions towards the community, bot, software, youtube, and other projects.\n→ To become a supporter, support on [Patreon](https://patreon.com/narlock)!\n\n</daily:{cfg.DAILY_COMMAND_ID}> Retrieve daily tokens!\n\nMore to come soon!')
        await interaction.response.edit_message(embed=self.embed, view=self)

class Help:
    @staticmethod
    def get_help_embed():
        embed = discord.Embed(title=f'Help', color=0xffa500)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='🛠️ General', value=GENERAL_HELP_VALUE, inline=False)
        embed.add_field(name='\u200b', value=f'Use the buttons below to get help on specific server features!\nNew to Discord? Visit <#{cfg.INFO_CHANNEL_ID}>!', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed