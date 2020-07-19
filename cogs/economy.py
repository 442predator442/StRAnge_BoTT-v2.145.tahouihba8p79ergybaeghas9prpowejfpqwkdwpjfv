import discord
from discord.ext import commands
import asyncio
import time

class economy(commands.Cog):
	def __init__(self, bot):
		self.Bot = bot



def setup(bot):
	bot.add_cog(economy(bot))
	print('[LOGS]: библиотека ECONOMY успешно загружена.')