"""
todo.py
author: narlock

Interface providing a simple todo list
"""

import cfg
import discord

from client.alder.interface.todo_client import TodoClient
from client.alder.interface.user_client import UserClient

number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

class Todo():
    def get_todo_list(self, interaction: discord.Interaction):
        TodoClient.delete_old_completed_todo_items_for_user(interaction.user.id)
        incomplete_items = TodoClient.get_incomplete_todo_items_for_user_content(interaction.user.id)
        completed_items = TodoClient.get_complete_todo_items_for_user_content(interaction.user.id)

        if not incomplete_items:
            incomplete_items_str = 'No items in Todo List!'
        else:
            incomplete_items_str = ""
            for index, item in enumerate(incomplete_items):
                if index == 9:
                    incomplete_items_str += f":keycap_ten: {item['item_name']}\n"
                    break
                incomplete_items_str += f":{number_words[index]}: {item['item_name']}\n"
        
        if not completed_items:
            completed_items_str = ''
        else:
            completed_items_str = '**Completed Today**\n\n'
            for index, item in enumerate(completed_items):
                completed_items_str += f":white_check_mark: {item['item_name']}\n"

        embed = self.get_sample_embed(interaction)
        embed.add_field(name='\u200b', value=incomplete_items_str, inline=False)

        if completed_items:
            embed.add_field(name='\u200b', value=completed_items_str, inline=False)
        
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed

    def clear_items(self, interaction: discord.Interaction):
        """
        Clear your entire todo list
        """
        TodoClient.delete_all_todo_items_for_user(interaction.user.id)
        embed = self.get_sample_embed(interaction)
        embed.add_field(name='\u200b', value='No items in Todo List!', inline=False)
        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def check_item(self, interaction: discord.Interaction, item_no):
        """
        Mark an active todo item as complete
        """
        incomplete_items = TodoClient.get_incomplete_todo_items_for_user_content(interaction.user.id)
        for index, item in enumerate(incomplete_items):
            if (index + 1) == item_no:
                TodoClient.complete_todo_item(item['id'])
        
        return self.get_todo_list(interaction)

    def remove_item(self, interaction: discord.Interaction, item_no):
        """
        Remove an active todo item from your todo list
        """
        incomplete_items = TodoClient.get_incomplete_todo_items_for_user_content(interaction.user.id)

        for index, item in enumerate(incomplete_items):
            if (index + 1) == item_no:
                TodoClient.delete_todo_item(item['id'])

        return self.get_todo_list(interaction)

    def add_item(self, interaction: discord.Interaction, item_name):
        """
        Add an item to your todo list: limit 10 items per user
        """
        incomplete_items = TodoClient.get_incomplete_todo_items_for_user_content(interaction.user.id)

        if len(incomplete_items) >= 10:
            return cfg.ErrorEmbed.message('You can only have 10 todo items open at a time!')
        else:
            TodoClient.create_todo_item(interaction.user.id, item_name)
        
        return self.get_todo_list(interaction)

    def update_item(self, interaction: discord.Interaction, item_no, update_item_name):
        """
        Update an item in todo list
        """
        incomplete_items = TodoClient.get_incomplete_todo_items_for_user_content(interaction.user.id)

        for index, item in enumerate(incomplete_items):
            if (index + 1) == item_no:
                TodoClient.update_todo_item_name(item['id'], update_item_name)

        return self.get_todo_list(interaction)
    
    def get_sample_embed(self, interaction: discord.Interaction):
        color = UserClient.get_discord_user_embed_color(interaction.user.id)
        embed = discord.Embed(title=f'📝 {interaction.user.name}\'s Todo List', color=color)
        try:
            embed.set_thumbnail(url=f'{interaction.user.avatar.url}')
        except Exception as e:
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        return embed