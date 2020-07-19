import discord
from discord.ext import commands
import asyncio
import sqlite3

sqlite_verify = 'db/Verify.db'

class verific(commands.Cog):
	def __init__(self, bot):
		self.Bot = bot


	db = sqlite3.connect(sqlite_verify)
	cursor = db.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS verole(
		vrole BIGINT,
		guildid BIGINT)""")
	db.commit()
	db.close()


	@commands.command(aliases = ['verific-role','v-role'])
	@commands.has_permissions(administrator = True)
	async def verificrole(self, ctx, arg: str, role: discord.Role = None):
		db = sqlite3.connect(sqlite_verify)
		cursor = db.cursor()
		cursor.execute(f"SELECT vrole FROM verole WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if arg =='enable':
			if role == None:
				emb = discord.Embed(
					description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\n**Использовать:**\n``verific-role [enable/disable] (@роль)``',
					colour = discord.Colour.red()
					)
				emb.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				await ctx.send(embed = emb)

			else:
				if not res:
					cursor.execute(f"INSERT INTO verole VALUES('{role.id}','{ctx.message.guild.id}')")
					db.commit()
					await ctx.send('***<:check:731024265826140311>Роль верификации успешно установлена***')
				else:
					cursor.execute(f"UPDATE verole SET vrole='{role.id}' WHERE guildid='{ctx.message.guild.id}'")
					db.commit()
					await ctx.send('***<:check:731024265826140311>Роль верификации успешно обновлена***')

		elif arg =='disable':
			if role == None:
				if not res:
					await ctx.send('***<:xmark:731024248222777374>На этом сервере и так не указана роль верификации!***')
				else:
					cursor.execute(f"DELETE FROM verole WHERE guildid='{ctx.message.guild.id}'")
					db.commit()
					await ctx.send('***<:check:731024265826140311>Роль верификации успешно сброшена***')
		db.close()
		

	@verificrole.error
	async def verificrole_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`verific-role [enable/disable] (@роль)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`verific-role enable @верифик`\n`verific-role disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`verificrole`, `v-role`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`verific-role [enable/disable] (@роль)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`verific-role enable @верифик`\n`verific-role disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`verificrole`, `v-role`', inline = False)
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(verific(bot))
	print('[LOGS]: библиотека VERIFIC успешно загружена.')
