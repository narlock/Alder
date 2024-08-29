"""
trivia.py
author: narlock

Alder interface for trivia question arcade game.
"""

import cfg
import discord

from tools.log import Logger
from client.alder.interface.triviaquestion_client import TriviaQuestionClient
from client.alder.interface.user_client import UserClient

class TriviaButtons(discord.ui.View):
    def __init__(self, embed: discord.Embed, user_id: int):
        super().__init__(timeout=None)
        self.embed = embed
        self.user_id = user_id

        self.dbresponse = TriviaQuestionClient.get_random_trivia_question_contents()
        Logger.debug(f'Random trivia response: {self.dbresponse}')
        self.question = f'**Category**: {self.dbresponse['category']}\n**By**: {self.dbresponse['author']}\n\n**{self.dbresponse['title']}**'
        self.options = [self.dbresponse['option_a'], self.dbresponse['option_b'], self.dbresponse['option_c'], self.dbresponse['option_d']]
        self.correct = self.dbresponse['correct']

        self.options_message = f'**A**: {self.options[0]}\n**B**: {self.options[1]}\n**C**: {self.options[2]}\n**D**: {self.options[3]}'
        self.embed.set_field_at(0, name='\u200b', value=self.question, inline=False)
        self.embed.set_field_at(1, name='\u200b', value=self.options_message, inline=False)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if the user who clicked the button is the same as the user who initiated the game."""
        return interaction.user.id == self.user_id

    @discord.ui.button(label='A', style=discord.ButtonStyle.blurple)
    async def option_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'**Category**: {self.dbresponse['category']}\n**By**: {self.dbresponse['author']}\n\nYou selected **A**', inline=False)
        self.check_correct_answer(interaction, 0)
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='B', style=discord.ButtonStyle.blurple)
    async def option_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'**Category**: {self.dbresponse['category']}\n**By**: {self.dbresponse['author']}\n\nYou selected **B**', inline=False)
        self.check_correct_answer(interaction, 1)
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='C', style=discord.ButtonStyle.blurple)
    async def option_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'**Category**: {self.dbresponse['category']}\n**By**: {self.dbresponse['author']}\n\nYou selected **C**', inline=False)
        self.check_correct_answer(interaction, 2)
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='D', style=discord.ButtonStyle.blurple)
    async def option_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(0, name='\u200b', value=f'**Category**: {self.dbresponse['category']}\n**By**: {self.dbresponse['author']}\n\nYou selected **D**', inline=False)
        self.check_correct_answer(interaction, 3)
        self.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self)

    def check_correct_answer(self, interaction: discord.Interaction, selection: int):
        print(f'selection:{selection} and self.correct={self.correct}')
        won_status = selection == self.correct
        wins = self.update_wins(won_status, interaction)
        if won_status:
            self.embed.color = discord.Color.green()
            self.embed.set_field_at(1, name='\u200b', value=f'You answered correctly!\nYou now have `{wins}` trivia questions correctly answered.', inline=False)
        else:
            self.embed.color = discord.Color.red()
            self.embed.set_field_at(1, name='\u200b', value=f'You answered incorrectly!\nYou have `{wins}` trivia questions correctly answered.', inline=False)
    
    def update_wins(self, won_status, interaction: discord.Interaction) -> int:
        if won_status:
            UserClient.add_trivia_win_for_user(interaction.user.id)
        return UserClient.get_user_trivia(interaction.user.id)

class Trivia():
    """
    Plays the trivia game.
    """
    def play_trivia(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Trivia Question for {interaction.user.name}", color=0xffa500)
        embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        embed.add_field(name='\u200b', value='', inline=False)
        embed.add_field(name='\u200b', value='', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed