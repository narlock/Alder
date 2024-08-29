"""
motivation.py
author: narlock

Simple interface for providing motivation to calling user.
"""

import discord
import random

class Motivation:

    @staticmethod
    def get_motivation_embed(interaction: discord.Interaction, user: discord.User):
        member = interaction.guild.get_member(interaction.user.id)
        
        if user is not None and isinstance(user, discord.member.Member):
            username = user.mention
        else:
            username = member.nick if member.nick is not None else member.name
        
        messages = [
            f"You got this, **{username}**!",
            f"Believe in yourself, **{username}**!",
            f"Keep pushing forward, **{username}**!",
            f"Stay strong, **{username}**!",
            f"You're capable of great things, **{username}**!",
            f"Don't give up, **{username}**!",
            f"Take it one step at a time, **{username}**!",
            f"You're making progress, **{username}**!",
            f"Stay focused and determined, **{username}**!",
            f"Success is within reach, **{username}**!",
            f"Never stop trying, **{username}**!",
            f"Keep your head up, **{username}**!",
            f"Stay positive and keep moving forward, **{username}**!",
            f"You're on the path to greatness, **{username}**!",
            f"You have what it takes to succeed, **{username}**!",
            f"Believe in yourself and your abilities, **{username}**!",
            f"Stay motivated and keep working hard, **{username}**!",
            f"Your hard work will pay off, **{username}**!",
            f"Never give up on your dreams, **{username}**!",
            f"Stay committed and you will achieve your goals, **{username}**!",
            f"Your perseverance will lead to success, **{username}**!",
            f"Stay driven and determined, **{username}**!",
            f"You're an inspiration, **{username}**!",
            f"Keep pushing through the challenges, **{username}**!",
            f"Success is a journey, not a destination, **{username}**!",
            f"Your dedication is admirable, **{username}**!",
            f"Stay motivated and you will overcome any obstacle, **{username}**!",
            f"Believe in yourself and you can achieve anything, **{username}**!",
            f"You're capable of achieving greatness, **{username}**!",
            f"Keep chasing your dreams, **{username}**!",
            f"You have the strength and determination to succeed, **{username}**!",
            f"Stay focused on your goals, **{username}**!",
            f"Your hard work and determination will pay off, **{username}**!",
            f"Believe you can and you're halfway there, **{username}**.",
            f"The only way to do great work is to love what you do, **{username}**.",
            f"Believe in yourself, take on your challenges, dig deep within yourself to conquer fears. Never let anyone bring you down, **{username}**.",
            f"If you can dream it, you can achieve it, **{username}**.",
            f"Success is not final, failure is not fatal: it is the courage to continue that counts, **{username}**.",
            f"Believe in your potential and you will go far, **{username}**.",
            f"Every great story begins with a hero, and you are the hero of your story, **{username}**.",
            f"The greatest glory in living lies not in never falling, but in rising every time we fall, **{username}**.",
            f"Stay motivated and you will reach your full potential, **{username}**!",
            f"You're an unstoppable force, **{username}**!",
            f"Keep pushing past your limits, **{username}**!",
            f"Stay positive and you will achieve greatness, **{username}**!",
            f"Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle, **{username}**.",
            f"Don't watch the clock; do what it does. Keep going, **{username}**.",
            f"You can't go back and change the beginning, but you can start where you are and change the ending, **{username}**.",
            f"The secret of getting ahead is getting started, **{username}**.",
            f"You are never too old to set another goal or to dream a new dream, **{username}**.",
            f"I can't change the direction of the wind, but I can adjust my sails to always reach my destination, **{username}**.",
            f"It does not matter how slowly you go as long as you do not stop, **{username}**.",
            f"Start where you are. Use what you have. Do what you can, **{username}**.",
            f"Believe in yourself and you will be unstoppable, **{username}**.",
            f"The only way to do great work is to love what you do, **{username}**.",
            f"Don't let yesterday take up too much of today, **{username}**.",
            f"**{username}**, you are not a product of circumstances; you are a product of decisions.",
            f"Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle, **{username}**.",
            f"The best way to predict your future is to create it, **{username}**.",
            f"Don't be pushed around by the fears in your mind. Be led by the dreams in your heart, **{username}**.",
            f"The way to get started is to quit talking and begin doing, **{username}**.",
            f"**{username}**, all the great performers I have worked with are fueled by a personal dream.",
            f"**{username}**, time stays long enough for anyone who will use it.",
            f"**{username}**, setting an example is not the main means of influencing another, it is the only means."
        ]

        return random.choice(messages)