import discord
from discord.ext import commands
import asyncio
import requests
import sqlite3

sqlite_sug = 'db/Suggest.db'


class general(commands.Cog):
	def __init__(self, bot):
		self.Bot = bot

	db = sqlite3.connect(sqlite_sug)
	cur = db.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS suggestion(
		schannel BIGINT,
		guildid BIGINT)""")
	db.commit()
	db.close()


	@commands.command()
	async def avatar (self, ctx, member: discord.Member = None):
		if member == None:
			user = ctx.message.author
		else:
			user = member
		emb = discord.Embed (title = f'Avatar "{user.name}":', colour = discord.Colour.green())
		emb.set_image(url = user.avatar_url)
		await ctx.send (embed = emb)


	@commands.command()
	async def suggest(self, ctx, *, arg: str):
		db = sqlite3.connect(sqlite_sug)
		cursor = db.cursor()
		cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			await ctx.send('**На этом сервере система идей отключена!**\n*Подключить систему идей* - ``suggestions [enable/disable] (#канал)``')
		else:
			for i in cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'"):
				suggest = i[0]
				sug = ctx.guild.get_channel(suggest)
				
				emb = discord.Embed( 
					description= f'{arg}', 
					colour = ctx.message.author.colour
					)
				emb.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				msg = await web.send(embed = emb)
				await bot.add_reaction('<:check:731024265826140311>')
				await bot.add_reaction('<:neutral:731024278623092776>')
				await bot.add_reaction('<:xmark:731024248222777374>')
				await ctx.send('***Ваша идея успешно отправлена! ✅***')
		db.close()


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def suggestions(self, ctx, arg:str, channel: discord.TextChannel = None):
		db = sqlite3.connect(sqlite_sug)
		cursor = db.cursor()
		cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()

		if arg =='enable':
			if not res:
				cursor.execute(f"INSERT INTO suggestion VALUES('{channel.id}','{ctx.message.guild.id}')")
				db.commit()
				await ctx.send('***Канал для идей успешно установлен*** ✅')

			else:
				cursor.execute(f"UPDATE suggestion SET schannel='{channel.id}' WHERE guildid='{ctx.message.guild.id}'")
				db.commit()
				await ctx.send('***Канал идей успешно обновлен*** ✅')

		elif arg =='disable':
			if channel == None:
				if not res:
					await ctx.send('***<:xmark:731024248222777374>На сервере уже отключена система идей!***')

				else:
					cursor.execute(f"DELETE FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
					db.commit()
					await ctx.send('***Система идей успешно отключена*** ✅')

		else:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите правильно все аргументы!**\n\n**Использовать:**\n``suggestions [enable/disable] (#канал_для_идей)``',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)
		db.close()


	@suggest.error
	async def suggest_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '<:xmark:731024248222777374>**Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`suggest [идея]`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`suggest подключить верификацию`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`suggest`', inline = False)
			await ctx.send(embed = emb)


	@suggestions.error
	async def suggestions_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '<:xmark:731024248222777374>**Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`suggestions [enable/disable] (#канал)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`suggestions enable #идеи-для-сервера`\n`suggestions disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`suggestions`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '<:xmark:731024248222777374>**Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`suggestions [enable/disable] (#канал)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`suggestions enable #идеи-для-сервера`\n`suggestions disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`suggestions`', inline = False)
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(general(bot))
	print('[LOGS]: библиотека GENERAL успешно загружена.')