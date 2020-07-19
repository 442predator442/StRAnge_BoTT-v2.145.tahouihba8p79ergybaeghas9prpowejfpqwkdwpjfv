import discord
from discord.ext import commands
import asyncio
import time

class rank(commands.Cog):
	def __init__(self, bot):
		self.Bot = bot



def setup(bot):
	bot.add_cog(rank(bot))
	print('[LOGS]: библиотека RANK успешно загружена.')