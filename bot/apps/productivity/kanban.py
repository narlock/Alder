"""
kanban.py
author: narlock

Kanban productivity board interface.
"""

import cfg
import discord

from client.alder.interface.kanban_client import KanbanClient
from client.alder.interface.user_client import UserClient

class Kanban():
    def get_priority(self, priority_number):
        if priority_number == 1:
            return "🔵"
        elif priority_number == 2:
            return "🟡"
        else:
            return "🔴"

    def view_kanban_board(self, interaction: discord.Interaction):
        items_by_column = KanbanClient.get_user_kanban_items_by_user_id_content(interaction.user.id)
        if items_by_column is None:
            return cfg.ErrorEmbed.message('Unable to connect to Kanban Client.\nPlease contact server administrator.')

        embed = self.get_sample_embed(interaction)

        todo_item_string = ''
        doing_item_string = ''
        done_item_string = ''

        # Function to construct item string based on format requirements
        def construct_item_string(item):
            item_string = f"[**{item['id']}**] {item['item_name']}"

            # Append tag if available
            if item['tag_name']:
                item_string += f" [**{item['tag_name']}**]"

            # Append velocity if available
            if item['velocity']:
                item_string += f" [**{item['velocity']}**]"

            # Append priority if available
            if item['priority_number']:
                item_string += f" {self.get_priority(item['priority_number'])}"

            return item_string

        # Iterate through items in the "todo" column
        for item in items_by_column['todo'][:5]:
            todo_item_string += construct_item_string(item) + "\n\n"

        # Iterate through items in the "doing" column
        for item in items_by_column['doing'][:5]:
            doing_item_string += construct_item_string(item) + "\n\n"

        # Iterate through items in the "done" column
        for item in items_by_column['done'][:5]:
            done_item_string += construct_item_string(item) + "\n\n"

        # Remove the last "\n\n" in each string
        todo_item_string = todo_item_string.rstrip("\n\n")
        doing_item_string = doing_item_string.rstrip("\n\n")
        done_item_string = done_item_string.rstrip("\n\n")

        embed.add_field(name='📌 Todo', value=todo_item_string)
        embed.add_field(name='🚧 Doing', value=doing_item_string)
        embed.add_field(name='✅ Done', value=done_item_string)

        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed
    
    def view_kanban_board_tag(self, interaction: discord.Interaction, tag):
        items_by_column = KanbanClient.get_user_kanban_items_by_tag_content(interaction.user.id, tag)
        if items_by_column is None:
            return cfg.ErrorEmbed.message('Unable to connect to Kanban Client.\nPlease contact server administrator.')
        
        embed = self.get_sample_embed(interaction)

        todo_item_string = ''
        doing_item_string = ''
        done_item_string = ''
        
        # Function to construct item string based on format requirements
        def construct_item_string(item):
            item_string = f"[**{item['id']}**] {item['item_name']}"

            # Append tag if available
            if item['tag_name']:
                item_string += f" [**{item['tag_name']}**]"

            # Append velocity if available
            if item['velocity']:
                item_string += f" [**{item['velocity']}**]"

            # Append priority if available
            if item['priority_number']:
                item_string += f" {self.get_priority(item['priority_number'])}"

            return item_string

        # Iterate through items in the "todo" column
        for item in items_by_column['todo'][:5]:
            todo_item_string += construct_item_string(item) + "\n\n"

        # Iterate through items in the "doing" column
        for item in items_by_column['doing'][:5]:
            doing_item_string += construct_item_string(item) + "\n\n"

        # Iterate through items in the "done" column
        for item in items_by_column['done'][:5]:
            done_item_string += construct_item_string(item) + "\n\n"

        # Remove the last "\n\n" in each string
        todo_item_string = todo_item_string.rstrip("\n\n")
        doing_item_string = doing_item_string.rstrip("\n\n")
        done_item_string = done_item_string.rstrip("\n\n")

        embed.add_field(name='📌 Todo', value=todo_item_string)
        embed.add_field(name='🚧 Doing', value=doing_item_string)
        embed.add_field(name='✅ Done', value=done_item_string)

        embed.add_field(name='\u200b', value=cfg.EMBED_FOOTER_STRING, inline=False)
        return embed

    def add_kanban_item(self, interaction: discord.Interaction, name, priority, tag, velocity):
        KanbanClient.create_kanban_item(interaction.user.id, name, priority, tag, velocity)
        if tag:
            return self.view_kanban_board_tag(interaction, tag)
        else:
            return self.view_kanban_board(interaction)

    def move_kanban_item(self, interaction: discord.Interaction, kanban_id):
        KanbanClient.move_kanban_item_column(kanban_id, interaction.user.id)
        return self.view_kanban_board(interaction)

    def update_kanban_item(self, interaction: discord.Interaction, kanban_id, name, priority, tag, velocity):
        KanbanClient.update_kanban_details_with_priority_tag_velocity(kanban_id, interaction.user.id, name, priority, tag, velocity)
        
        if tag:
            return self.view_kanban_board_tag(interaction, tag)
        else:
            return self.view_kanban_board(interaction)

    def remove_kanban_item(self, interaction: discord.Interaction, kanban_id):
        KanbanClient.delete_user_kanban_item(interaction.user.id, kanban_id)
        return self.view_kanban_board(interaction)

    def move_kanban_item_to_column(self, interaction: discord.Interaction, kanban_id, column):
        KanbanClient.move_kanban_item_column(kanban_id, interaction.user.id, column)
        return self.view_kanban_board(interaction)
    
    def complete(self, interaction: discord.Interaction):
        KanbanClient.delete_completed_user_kanban_items(interaction.user.id)
        return self.view_kanban_board(interaction)

    def get_sample_embed(self, interaction: discord.Interaction):
        color = UserClient.get_discord_user_embed_color(interaction.user.id)
        embed = discord.Embed(title=f'🗂️ {interaction.user.name}\'s Kanban Board', color=color)
        try:
            embed.set_thumbnail(url=f'{interaction.user.avatar.url}')
        except Exception as e:
            embed.set_thumbnail(url=cfg.DISCORD_ALDER_IMAGE_URL)
        return embed
    