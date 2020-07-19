import discord
from discord.ext import commands
import time
import asyncio
import requests
import sqlite3

sqlite_mod = 'db/Moderation.db'


class moderation(commands.Cog):
	def __init__(self, bot):
		self.Bot = bot

	db = sqlite3.connect(sqlite_mod)
	cursor = db.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS modrole(
		modrole BIGINT,
		guildid BIGINT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS mute(
		muterole BIGINT,
		guildid BIGINT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS modlog(
		mlchannel BIGINT,
		guildid BIGINT)""")
	db.commit()
	db.close()


	@commands.command(aliases = ['cls'])
	@commands.has_permissions(manage_messages = True)
	async def clear (self, ctx, amount: int):
		await ctx.message.delete()
		await ctx.channel.purge( limit =  amount)
		emb = discord.Embed(description = f'<:check:731024265826140311>Было удалено {amount} сообщений', colour = discord.Colour.red())
		await ctx.send(embed = emb, delete_after= 5.0)


	@commands.command()
	async def warn(self, ctx, member: discord.Member, *, reason = None):
		if member == ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете выдать предуприждение самому себе!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
		else:
			db = sqlite3.connect(sqlite_mod)
			cursor = db.cursor()
			cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send('**<:xmark:731024248222777374>На сервере не указана роль модератора!**\n\n*Указать роль модератора:* ``mod-role [enable/disable] (@роль)``')
			else:
				for i in cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'"):
					mr = i[0]
					mrole = ctx.guild.get_role(mr)
					roles = ctx.author.roles
					if mrole in roles:
						embed = discord.Embed(
							description = f'***<:check:731024265826140311>Участнику {member.mention} было успешно выдано устное предуприждение***',
							colour = discord.Colour.green()
							)
						embed.set_author(
							name = f'{ctx.author.name}#{ctx.author.discriminator}',
							icon_url = ctx.author.avatar_url
							)
						await ctx.send(embed = embed)
						guild = ctx.guild

						emb = discord.Embed(
							description = f'**Сервер:** {ctx.guild.name}\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Предуприждение``\n**Причина:** ``{reason}``',
							colour = discord.Colour.gold()
							)
						if ctx.author == ctx.message.guild.owner:
							await member.send(embed = emb)
						else:
							await member.send(embed = emb)
						cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
						rese = cursor.fetchall()

						if not rese:
							return

						else:
							for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
								mlchannel = i[0]
								mlch = ctx.guild.get_channel(mlchannel)
								embed = discord.Embed(
									description = f'**Участник:** {member.mention}\n**Действие:** ``Предуприждение``\n**Причина:** ``{reason}``',
									colour = discord.Colour.gold()
									)
								embed.set_author(
									name = f'{ctx.author.name}#{ctx.author.discriminator}',
									icon_url = ctx.author.avatar_url
									)
								await mlch.send(embed = embed)
					else:
						emb = discord.Embed(
							description = '**<:xmark:731024248222777374>У вас недостаточно прав на использование данной команды!**',
							colour = discord.Colour.red()
							)
						emb.set_author(
							name = f'{ctx.author.name}#{ctx.author.discriminator}',
							icon_url = ctx.author.avatar_url
							)
						await ctx.send(embed = emb)
						db.close()


	@commands.command(aliases = ['t-mute','tm','temp-mute'])
	async def tempmute(self, ctx, member: discord.Member, duration, *, reason = None):
		if member ==ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете выдать мут самому себе!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			return
		else:
			db = sqlite3.connect(sqlite_mod)
			cursor = db.cursor()
			cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send('**<:xmark:731024248222777374>На этом сервере не указана роль модератора!**\n\n*Указать роль модератора:* ``mod-role [enable/disable] (@роль)``')
			else:
				for i in cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'"):
					mr = i[0]
					mrole = ctx.guild.get_role(mr)
					roles = ctx.message.author.roles
					if mrole in roles:
						cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'")
						ress = cursor.fetchall()
						if not ress:
							await ctx.send('**<:xmark:731024248222777374>На этом сервере не указана мут-роль!**\n\n*Указать мут-роль:* ``mute-role [enable/disable] (@роль)``')
						else:
							for i in cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'"):
								muter = i[0]
								muterole = ctx.message.guild.get_role(muter)
								await member.add_roles(muterole)
								unit = duration[-1]
								if unit == 's':
									time = int(duration[:-1])
									longunit = 'секунд'
								elif unit == 'm':
									time = int(duration[:-1]) * 60
									longunit = 'минут'
								elif unit == 'h':
									time = int(duration[:-1]) * 60 * 60
									longunit = 'часов'
								elif unit == 'd':
									time = int(duration[:-1]) * 60 * 60 * 24
									longunit = 'дней'
								else:
									emb = discord.Embed(
										description = '**<:xmark:731024248222777374>Введите корректно время!**\n\nПримеры формата времени: `1s`, `1m`, `1h`, `1d`',
										colour = discord.Colour.red()
										)
									emb.add_field(name = 'Использовать:', value = '`tempmute [@участник] [время] (причина)`', inline = False)
									emb.add_field(name = 'Примеры:', value = '`tempmute @участник 1h`\n`tempmute @участник 1d нарушение правил`', inline = False)
									emb.add_field(name = 'Псевдонимы:', value = '`tempmute`, `tmute`, `tm`')
									await ctx.send(embed = emb)
									return
								emb = discord.Embed(
									description = f'{member.mention} был замьючен на {int(duration[:-1])} {longunit}',
									colour = discord.Colour.green()
									)
								emb.set_author(
									name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
									icon_url = ctx.message.author.avatar_url
									)
								embed = discord.Embed(
									description = f'**Сервер:** ``{ctx.message.guild.name}``\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Временный мут.``\n**Время:** ``{int(duration[:-1])} {longunit}``\n**Причина:** ``{reason}``',
									colour = discord.Colour.gold()
									)
								await ctx.send(embed = emb)
								await member.send(embed = embed)
								cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
								rese = cursor.fetchall()
								if not res:
									pass
								else:
									for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
										mlchannel = i[0]
										mlch = ctx.message.guild.get_channel(mlchannel)
										emb = discord.Embed(
											description = f'**Участник:** {member.mention}\n**Действие:** ``Временный мут``\n**Время:** ``{int(duration[:-1])} {longunit}``\n**Причина:** ``{reason}``',
											colour = discord.Colour.gold()
											)
										emb.set_author(
											name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
											icon_url = ctx.author.avatar_url
											)
										await mlch.send(embed = emb)
										await asyncio.sleep(time)
										uroles = member.roles
										if muterole in uroles:
											await member.remove_roles(muterole)
											embeed = discord.Embed(
												description = f'**Сервер:** ``{ctx.message.guild.name}``\n**Действие от:** {ctx.message.author.mention}\n**Действие:** ``Розблокировка чата.``\n**Причина:** ``Автоматическая розблокировка чата.``',
												colour = discord.Colour.green()
												)
											emd = discord.Embed(
												description = f'**Участник:** {member.mention}\n**Действие:** ``Розблокировка чата.``\n**Причина:** ``Автоматическая розблокировка чата.``',
												colour = discord.Colour.green()
												)
											emd.set_author(
												name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
												icon_url = ctx.message.author.avatar_url
												)
											await member.send(embed = embeed)
											await mlch.send(embed = emd)
										else:
											pass
					elif ctx.message.author == ctx.message.guild.owner:
						cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'")
						ress = cursor.fetchall()
						if not ress:
							await ctx.send('**<:xmark:731024248222777374>На этом сервере не указана мут-роль!**\n\n*Указать мут-роль:* ``mute-role [enable/disable] (@роль)``')
						else:
							for i in cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'"):
								muter = i[0]
								muterole = ctx.message.guild.get_role(muter)
								await member.add_roles(muterole)
								unit = duration[-1]
								if unit == 's':
									time = int(duration[:-1])
									longunit = 'секунд'
								elif unit == 'm':
									time = int(duration[:-1]) * 60
									longunit = 'минут'
								elif unit == 'h':
									time = int(duration[:-1]) * 60 * 60
									longunit = 'часов'
								elif unit == 'd':
									time = int(duration[:-1]) * 60 * 60 * 24
									longunit = 'дней'
								else:
									emb = discord.Embed(
										description = '**<:xmark:731024248222777374>Введите корректно время!**\n\nПримеры формата времени: `1s`, `1m`, `1h`, `1d`',
										colour = discord.Colour.red()
										)
									emb.add_field(name = 'Использовать:', value = '`tempmute [@участник] [время] (причина)`', inline = False)
									emb.add_field(name = 'Примеры:', value = '`tempmute @участник 1h`\n`tempmute @участник 1d нарушение правил`', inline = False)
									emb.add_field(name = 'Псевдонимы:', value = '`tempmute`, `tmute`, `tm`')
									await ctx.send(embed = emb)
									return
								emb = discord.Embed(
									description = f'{member.mention} был успешно замьючен на {int(duration[:-1])} {longunit}',
									colour = discord.Colour.green()
									)
								emb.set_author(
									name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
									icon_url = ctx.message.author.avatar_url
									)
								embed = discord.Embed(
									description = f'**Сервер:** ``{ctx.message.guild.name}``\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Временный мут.``\n**Время:** ``{int(duration[:-1])} {longunit}``\n**Причина:** ``{reason}``',
									colour = discord.Colour.gold()
									)
								await ctx.send(embed = emb)
								await member.send(embed = embed)
								cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
								rese = cursor.fetchall()
								if not rese:
									pass
								else:
									for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
										mlchannel = i[0]
										mlch = ctx.message.guild.get_channel(mlchannel)
										emb = discord.Embed(
											description = f'**Участник:** {member.mention}\n**Действие:** ``Временный мут``\n**Время:** ``{int(duration[:-1])} {longunit}``\n**Причина:** ``{reason}``',
											colour = discord.Colour.gold()
											)
										emb.set_author(
											name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
											icon_url = ctx.author.avatar_url
											)
										await mlch.send(embed = emb)
										await asyncio.sleep(time)
										uroles = member.roles
										if muterole in uroles:
											await member.remove_roles(muterole)
											embeed = discord.Embed(
												description = f'**Сервер:** ``{ctx.message.guild.name}``\n**Действие от:** {ctx.message.author.mention}\n**Действие:** ``Розблокировка чата.``\n**Причина:** ``Автоматическая розблокировка чата.``',
												colour = discord.Colour.green()
												)
											emd = discord.Embed(
												description = f'**Участник:** {member.mention}\n**Действие:** ``Розблокировка чата.``\n**Причина:** ``Автоматическая розблокировка чата.``',
												colour = discord.Colour.green()
												)
											emd.set_author(
												name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
												icon_url = ctx.message.author.avatar_url
												)
											await member.send(embed = embeed)
											await mlch.send(embed = emd)
										else:
											pass

					else:
						emb = discord.Embed(
							description = '**<:xmark:731024248222777374>У вас недостаточно прав на использование данной команды!**',
							colour = discord.Colour.red()
							)
						emb.set_author(
							name = f'{ctx.author.name}#{ctx.author.discriminator}',
							icon_url = ctx.author.avatar_url
							)
						await ctx.send(embed = emb)
						db.close()


	@commands.command(aliases = ['un-mute'])
	async def unmute(self, ctx, member: discord.Member, *, reason = None):
		if member == ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете розмьютить самого себя!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			return
		else:
			db = sqlite3.connect(sqlite_mod)
			cursor = db.cursor()
			cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send('**<:xmark:731024248222777374>На сервере не указана роль модератора!**\n\n*Указать роль модератора:* ``mod-role [enable/disable] (@роль)``')
			else:
				for i in cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'"):
					mr = i[0]
					mrole = ctx.guild.get_role(mr)
					roles = ctx.author.roles

					if mrole in roles:
						cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'")
						ress = cursor.fetchall()
						if not ress:
							await ctx.send('**<:xmark:731024248222777374>На сервере не указана мут-роль!**\n\n*Указать мут-роль:* ``mute-role [enable/disable] (@роль)``')
						else:
							for i in cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'"):
								muter = i[0]
								muterole = ctx.guild.get_role(muter)
								uroles = member.roles
								if muterole in uroles:
									embed = discord.Embed(
										description = f'***<:check:731024265826140311>{member.mention} был успешно розмьючен***',
										colour = discord.Colour.green()
										)
									embed.set_author(
										name = f'{ctx.author.name}#{ctx.author.discriminator}',
										icon_url = ctx.author.avatar_url
										)
									emb = discord.Embed(
										description = f'**Сервер:** `{ctx.message.guild.name}`\n**Действие от:** {ctx.message.author.mention}\n**Действие:** `Розблокировка чата.`\n**Причина:** `{reason}`',
										colour = discord.Colour.green()
										)
									await ctx.message.channel.send(embed = embed)
									await member.remove_roles(muterole)
									await member.send(embed = emb)
									cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
									rese = cursor.fetchall()
									if not rese:
										pass
									else:
										for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
											mlchannel = i[0]
											mlch = ctx.message.guild.get_channel(mlchannel)
											em = discord.Embed(
												description = f'**Участник:** {member.mention}\n**Действие:** `Розблокировка чата`\n**Причина:** `{reason}`',
												colour = discord.Colour.green()
												)
											em.set_author(
												name = f'{ctx.author.name}#{ctx.author.discriminator}',
												icon_url = ctx.author.avatar_url
												)
											await mlch.send(embed = em)
								else:
									e = discord.Embed(
										description = f'<:xmark:731024248222777374>{ctx.message.author.mention}, **этот участник и так не имеет мут.**',
										colour = discord.Colour.red()
										)
									e.set_author(
										name = f'{ctx.author.name}#{ctx.author.discriminator}',
										icon_url = ctx.message.author.avatar_url
										)
									await ctx.message.channel.send(embed = e)
		db.close()
						



	@commands.command(aliases = ['chat-mute'])
	async def mute(self, ctx, member: discord.Member, *, reason = None):
		if member == ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете выдать мут самому себе!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			return
		else:
			db = sqlite3.connect(sqlite_mod)
			cursor = db.cursor()
			cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()

			if not res:
				await ctx.send('**<:xmark:731024248222777374>На сервере не указана роль модератора!**\n\n*Указать роль модератора:* ``mod-role [enable/disable] (@роль)``')

			else:
				for i in cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'"):
					mr = i[0]
					mrole = ctx.guild.get_role(mr)
					roles = ctx.author.roles
						
					if mrole in roles:
						embed = discord.Embed(
							description = f'***<:check:731024265826140311>{member.mention} был успешно замьючен***',
							colour = discord.Colour.green()
							)
						embed.set_author(
							name = f'{ctx.author.name}#{ctx.author.discriminator}',
							icon_url = ctx.author.avatar_url
							)
						await ctx.send(embed = embed)
						cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'")
						ress = cursor.fetchall()

						if not ress:
							await ctx.send('**<:xmark:731024248222777374>На сервере не указана мут-роль!**\n\n*Указать мут-роль:* ``mute-role [enable/disable] (@роль)``')

						else:
							for i in cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'"):
								mrole = i[0]
								muterole = ctx.guild.get_role(mrole)
								await member.add_roles(muterole)

								emb = discord.Embed(
									description = f'**Сервер:** ``{ctx.guild.name}``\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Мут``\n**Причина:** ``{reason}``',
									colour = discord.Colour.gold()
									)
								if ctx.author == ctx.message.guild.owner:
									await member.send(embed = emb)
								else:
									await member.send(embed = emb)
								cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
								rese = cursor.fetchall()

								if not rese:
									pass

								else:
									for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
										mlchannel = i[0]
										mlch = ctx.guild.get_channel(mlchannel)

										embed = discord.Embed(
											description = f'**Участник:** {member.mention}\n**Действие:** ``Мут``\n**Причина:** ``{reason}``',
											colour = discord.Colour.gold()
											)
										embed.set_author(
											name = f'{ctx.author.name}#{ctx.author.discriminator}',
											icon_url = ctx.author.avatar_url
											)
										await mlch.send(embed = embed)
					elif ctx.message.author == ctx.message.guild.owner:
						embed = discord.Embed(
							description = f'***<:check:731024265826140311>{member.mention} был успешно замьючен***',
							colour = discord.Colour.green()
							)
						embed.set_author(
							name = f'{ctx.author.name}#{ctx.author.discriminator}',
							icon_url = ctx.author.avatar_url
							)
						await ctx.send(embed = embed)
						cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'")
						ress = cursor.fetchall()

						if not ress:
							await ctx.send('**На сервере не указана мут-роль!**\n\n*Указать мут-роль:* ``mute-role [enable/disable] (@роль)``')

						else:
							for i in cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'"):
								mrole = i[0]
								muterole = ctx.guild.get_role(mrole)
								await member.add_roles(muterole)

								emb = discord.Embed(
									description = f'**Сервер:** ``{ctx.guild.name}``\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Мут``\n**Причина:** ``{reason}``',
									colour = discord.Colour.gold()
									)
								if ctx.author == ctx.message.guild.owner:
									await member.send(embed = emb)
								else:
									await member.send(embed = emb)
								cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
								rese = cursor.fetchall()

								if not rese:
									pass

								else:
									for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
										mlchannel = i[0]
										mlch = ctx.guild.get_channel(mlchannel)

										embed = discord.Embed(
											description = f'**Участник:** {member.mention}\n**Действие:** ``Мут``\n**Причина:** ``{reason}``',
											colour = discord.Colour.gold()
											)
										embed.set_author(
											name = f'{ctx.author.name}#{ctx.author.discriminator}',
											icon_url = ctx.author.avatar_url
											)
										await mlch.send(embed = embed)
					else:
						emb = discord.Embed(
							description = '<:xmark:731024248222777374>**У вас недостаточно прав на использование данной команды!**',
							colour = discord.Colour.red()
							)
						emb.set_author(
							name = f'{ctx.author.name}#{ctx.author.discriminator}',
							icon_url = ctx.author.avatar_url
							)
						await ctx.send(embed = emb)
						db.close()


	@commands.command(aliases = ['b'])
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, member: discord.Member, *, reason = None):
		db = sqlite3.connect(sqlite_mod)
		cursor = db.cursor()
		cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if member == ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете забанить самого себя!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			return

		else:
			await ctx.send(f'***<:check:731024265826140311>{member.mention} был успешно забанен***')

			embed = discord.Embed(
				description = f'**Сервер:** {ctx.guild.name}\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Бан``\n**Причина:** ``{reason}``',
				colour = discord.Colour.red()
				)
			await member.send(embed = embed)

			await asyncio.sleep(1)
			await member.ban(reason = reason)

			if not res:
				pass

			else:
				for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
					mlchannel = i[0]
					mlch = self.Bot.get_channel(mlchannel)
					embed = discord.Embed(
						description = f'**Участник:** {member.mention}\n**Действие:** ``Ban``\n**Причина:** ``{reason}``',
						colour = discord.Colour.gold()
						)
					embed.set_author(
						name = f'{ctx.author.name}#{ctx.author.discriminator}',
						icon_url = ctx.author.avatar_url
						)
					await mlch.send(embed = embed)
		db.close()


	@commands.command(aliases = ['temp-ban','t-ban','tb'])
	@commands.has_permissions(administrator = True)
	async def tempban(self, ctx, member: discord.Member, duration, *, reason = None):
		if member ==ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете выдать мут самому себе!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			return

		else:
			unit = duration[-1]
			if unit == 's':
				time = int(duration[:-1])
				longunit = 'секунд'
			elif unit == 'm':
				time = int(duration[:-1]) * 60
				longunit = 'минут'
			elif unit == 'h':
				time = int(duration[:-1]) * 60 * 60
				longunit = 'часов'
			elif unit == 'd':
				time = int(duration[:-1]) * 60 * 60 * 24
				longunit = 'дней'
			else:
				emb = discord.Embed(
					description = '**<:xmark:731024248222777374>Введите корректно время!**\n\nПримеры формата времени: `1s`, `1m`, `1h`, `1d`',
					colour = discord.Colour.red()
					)
				emb.add_field(name = 'Использовать:', value = '`tempmute [@участник] [время] (причина)`', inline = False)
				emb.add_field(name = 'Примеры:', value = '`tempmute @участник 1h`\n`tempmute @участник 1d нарушение правил`', inline = False)
				emb.add_field(name = 'Псевдонимы:', value = '`tempmute`, `tmute`, `tm`')
				await ctx.send(embed = emb)
				return
			emb = discord.Embed(
				description = f'{member.mention} был забанен на {int(duration[:-1])} {longunit}',
				colour = discord.Colour.green()
				)
			embed = discord.Embed(
				description = f'**Сервер:** `{ctx.message.guild.name}`\n**Действие от:** {ctx.message.author.mention}\n**Действие:** `Временный бан`\n**Время:** `{int(duration[:-1])} {longunit}`\n**Причина:** `{reason}`',
				colour = discord.Colour.red()
				)
			await ctx.message.channel.send(embed = emb)
			await member.send(embed = embed)
			await member.ban(reason = reason)
			await asyncio.sleep(time)
			db = sqlite3.connect(sqlite_mod)
			cursor = db.cursor()
			cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				pass
			else:
				for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
					mlchannel = i[0]
					mlch = ctx.guild.get_channel(mlchannel)
					em = discord.Embed(
						description = f'**Участник:** {member.mention}\n**Действие:** `Временный бан`\n**Время:** `{int(duration[:-1])} {longunit}`\n**Причина:** `{reason}`',
						colour = discord.Colour.red()
						)
					em.set_author(
						name = f'{ctx.author.name}#{ctx.author.discriminator}',
						icon_url = ctx.author.avatar_url
						)
					await mlch.send(embed = em)
			await asyncio.sleep(time)
			await member.unban()
			cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
			ress = cursor.fetchall()
			if not res:
				pass
			else:
				for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
					mlchannel = i[0]
					mlch = ctx.guild.get_channel(mlchannel)
					em = discord.Embed(
						description = f'**Участник:** {member.mention}\n**Действие:** `Розбан`\n**Причина:** `Автоматический розбан`',
						colour = discord.Colour.green()
						)
					em.set_author(
						name = f'{ctx.author.name}#{ctx.author.discriminator}',
						icon_url = ctx.author.avatar_url
						)
					await mlch.send(embed = em)


	@commands.command(aliases = ['un-ban'])
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, member:int = None):
		if member == ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете розбанить самого себя!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
		else:
			banned = await ctx.guild.bans()
			for ban_entry in banned:
				user = ban_entry.user
				if user.id == member:
					embed = discord.Embed(
						description = f'***<:check:731024265826140311>{user.mention} успешно розбанен***',
						colour = discord.Colour.green()
						)
					embed.set_author(
						name = f'{ctx.author.name}#{ctx.author.discriminator}',
						icon_url = ctx.author.avatar_url
						)
					await ctx.guild.unban(user)
					await ctx.send(embed = embed)
					db = sqlite3.connect(sqlite_mod)
					cursor = db.cursor()
					cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
					res = cursor.fetchall()
					if not res:
						return

					else:
						for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
							mlchannel = i[0]
							mlch = self.Bot.get_channel(mlchannel)
							emb = discord.Embed(
								description = f'**Участник:** {user.mention}\n**Действие:** ``Розбан``\n**Причина:** ``{reason}``',
								colour = discord.Colour.gold()
								)
							emb.set_author(
								name = f'{ctx.author.name}#{ctx.author.discriminator}',
								icon_url = ctx.author.avatar_url
								)
							await mlch.send(embed = emb)
			db.close()
			return

	@commands.command(aliases = ['b-list','bl','ban-list'])
	@commands.has_permissions(ban_members = True)
	async def banlist(self, ctx):
		bans = await ctx.guild.bans()
		if len(bans) == 0:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>На сервере нету забаненных участников.**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)
		else:
			em = discord.Embed(
				title=f'Список забаненых участников({len(bans)}):', 
				description = '\n'.join([str(b.user) for b in bans]),
				colour = discord.Colour.green()
				)
			await ctx.send(embed=em)


	@commands.command(aliases = ['mass-role'])
	@commands.has_permissions(administrator = True)
	async def massrole(self, ctx, arg: str, target: discord.Role, role: discord.Role):
		members = ctx.message.guild.members
		number_failed_add = 0
		number_failed_remove = 0
		number_add = 0
		number_remove = 0
		if arg =='add':
			emb = discord.Embed(
				description = f'Добавление роли {role.mention} к участникам с ролью {target.mention}.\nЭто может занять некоторое время.',
				colour = discord.Colour.blue()
				)
			emb.set_author(
				name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			start_time = time.time()
			for member in members:
				roles = member.roles
				if role in roles:
					pass
				elif target in roles:
					try:
						await member.add_roles(role)
						number_add += 1
					except Exception as error:
						number_failed_add += 1
			time_taken = time.time() - start_time
			if round(time_taken) ==[0]:
				time_taken = 1
			embed = discord.Embed(
				description = f'<:check:731024265826140311> Массовая роздача роли завершена.\n**Участников:** `{number_add}`\n**Не выдано по ошибке:** `{number_failed_add}`\n**Время:** `{round(time_taken)} секунд`',
				colour = discord.Colour.green())
			embed.set_author(
				name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = embed)
		elif arg =='remove':
			emb = discord.Embed(
				description = f'Удаление роли {role.mention} с участников, имеющие роль {target.mention}.\nЭто может занять некоторое время.',
				colour = discord.Colour.blue()
				)
			emb.set_author(
				name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
			start_time = time.time()
			for member in members:
				roles = member.roles
				if role in roles:
					pass
				elif target in roles:
					try:
						await member.remove_roles(role)
						number_remove += 1
					except Exception as error:
						number_failed_remove += 1
				else:
					pass
			time_taken = time.time() - start_time
			if round(time_taken) ==0:
				time_taken = 1
			embed = discord.Embed(
				description = f'<:check:731024265826140311> Массовое удаление роли завершена.\n**Участников:** `{number_remove}`\n**Не удалено по ошибке:** `{number_failed_remove}`\n**Время:** `{round(time_taken)} секунд`',
				colour = discord.Colour.green())
			embed.set_author(
				name = f'{ctx.message.author.name}#{ctx.message.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = embed)
		return


	@commands.command()
	@commands.has_permissions(kick_members = True)
	async def kick(self, ctx, member: discord.Member, *, reason = None):
		if member == ctx.message.author:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Вы не можете кикнуть самого себя!**',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.message.author.avatar_url
				)
			await ctx.send(embed = emb)
		else:
			db = sqlite3.connect(sqlite_mod)
			cursor = db.cursor()
			cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			await ctx.send(f'***<:check:731024265826140311>{member.mention} был успешно кикнут***')
			embed = discord.Embed(
				description = f'**Сервер:** {ctx.guild.name}\n**Действие от:** {ctx.author.mention}\n**Действие:** ``Кик``\n**Причина:** ``{reason}``',
				colour = discord.Colour.red()
				)
			await member.send(embed = embed)

			await asyncio.sleep(1)
			await member.kick(reason = reason)
			if not res:
				pass

			else:
				for i in cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'"):
					mlchannel = i[0]
					mlch = self.Bot.get_channel(mlchannel)
					embed = discord.Embed(
						description = f'**Участник:** {member.mention}\n**Действие:** ``Кик``\n**Причина:** ``{reason}``',
						colour = discord.Colour.gold()
						)
					embed.set_author(
						name = f'{ctx.author.name}#{ctx.author.discriminator}',
						icon_url = ctx.author.avatar_url
						)
					await mlch.send(embed = embed)
			db.close()


	@commands.command(aliases = ['mod-role'])
	@commands.has_permissions(administrator = True)
	async def modrole(self, ctx, arg:str, role: discord.Role = None):
		db = sqlite3.connect(sqlite_mod)
		cursor = db.cursor()
		cursor.execute(f"SELECT modrole FROM modrole WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()

		if arg =='enable':
			if not res:
				cursor.execute(f"INSERT INTO modrole VALUES('{role.id}','{ctx.message.guild.id}')")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Роль модератора успешно установлена***')

			elif role == None:
				emb = discord.Embed(
					description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\n**Использовать:**\n``mod-role [enable/disable] (@роль)``',
					colour = discord.Colour.red()
					)
				emb.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				await ctx.send(embed = emb)

			else:
				cursor.execute(f"UPDATE modrole SET modrole='{role.id}' WHERE guildid='{ctx.message.guild.id}'")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Роль модератора успешно обновлена***')

		elif arg in 'disable':
			if role == None:
				if not res:
					await ctx.send('***<:xmark:731024248222777374>На этом сервере и так не назначена роль модератора!***')

				else:
					cursor.execute(f"DELETE FROM modrole WHERE guildid='{ctx.message.guild.id}'")
					db.commit()
					await ctx.send('***<:check:731024265826140311>Роль модератора успешно сброшена***')
		db.close()


	@commands.command(aliases = ['mute-role'])
	@commands.has_permissions(administrator = True)
	async def muterole(self, ctx, arg:str, role: discord.Role = None):
		db = sqlite3.connect(sqlite_mod)
		cursor = db.cursor()
		cursor.execute(f"SELECT muterole FROM mute WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()

		if arg =='enable':
			if not res:
				cursor.execute(f"INSERT INTO mute VALUES('{role.id}','{ctx.message.guild.id}')")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Мут-роль успешно установлена***')

			else:
				cursor.execute(f"UPDATE mute SET muterole='{role.id}' WHERE guildid='{ctx.message.guild.id}'")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Мут-роль успешно обновлена***')

		elif arg =='disable':
			if role == None:
				if not res:
					await ctx.send('***На этом сервере и так не указана мут-роль!***')

				else:
					cursor.execute(f"DELETE FROM mute WHERE guildid='{ctx.message.guild.id}'")
					db.commit()
					await ctx.send('***<:check:731024265826140311>Мут-роль успешно сброшена***')

			else:
				emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите правильно все аргументы!**\n\n**Использовать:**\n``mute-role [enable/disable] (@роль)``',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)

		else:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите правильно все аргументы!**\n\n**Использовать:**\n``mute-role [enable/disable] (@роль)``',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)
		db.close()



	@commands.command(aliases = ['m-log','ml','mod-log'])
	@commands.has_permissions(administrator = True)
	async def modlog(self, ctx, arg:str, channel: discord.TextChannel = None):
		db = sqlite3.connect(sqlite_mod)
		cursor = db.cursor()
		cursor.execute(f"SELECT mlchannel FROM modlog WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if arg =='enable':
			if not res:
				cursor.execute(f"INSERT INTO modlog VALUES('{channel.id}','{ctx.message.guild.id}')")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Канал для логов модерации успешно установлен***')

			else:
				cursor.execute(f"UPDATE modlog SET mlchannel='{channel.id}' WHERE guildid='{ctx.message.guild.id}'")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Канал для логов модерации успешно обновлен***')

		elif arg=='disable':
			if channel == None:
				if not res:
					await ctx.send('***<:xmark:731024248222777374>На этом сервере логи модерации и так отключены!***')

				else:
					cursor.execute(f"DELETE FROM modlog WHERE guildid='{ctx.message.guild.id}'")
					db.cursor()
					await ctx.send('***<:check:731024265826140311>Логи модерации успешно отключены***')

			else:
				emb = discord.Embed(
					description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\n**Использовать:**\n``mod-log [enable/disable] (#канал_логов)``',
					colour = discord.Colour.red()
					)
				emb.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				await ctx.send(embed = emb)

		db.close()


	@clear.error
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`clear [к-во сообщений]`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`clear 15`', inline = False)
			emb.add_field(name = 'Права:', value = '`Управлять сообщениями`, `Администратор`, `Создатель сервера`')
			emb.add_field(name = 'Псевдонимы:', value = '`clear`, `cls`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`clear [к-во сообщений]`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`clear 15`', inline = False)
			emb.add_field(name = 'Права:', value = '`Управлять сообщениями`, `Администратор`, `Создатель сервера`')
			emb.add_field(name = 'Псевдонимы:', value = '`clear`, `cls`', inline = False)
			await ctx.send(embed = emb)

	@warn.error
	async def warn_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`warn [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`warn @участник`\n`warn @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Модератор`, `Администратор`, `Создатель сервера`')
			emb.add_field(name = 'Псевдонимы:', value = '`warn`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`warn [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`warn @участник`\n`warn @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Модератор`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`warn`', inline = False)
			await ctx.send(embed = emb)


	@mute.error
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mute [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mute @участник`\n`mute @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Модератор`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`mute`', inline = False)
			await ctx.send(embed = emb)


	@unmute.error
	async def unmute_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`un-mute [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`un-mute @участник`\n`un-mute @участник ошибочный мут`', inline = False)
			emb.add_field(name = 'Права:', value = '`Модератор`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`unmute`, `del-mute`', inline = False)
			await ctx.send(embed = emb)


	@unban.error
	async def unban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`un-ban [айди участника] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`un-ban 614424106242277416`\n`un-ban 614424106242277416 ошибочный бан`', inline = False)
			emb.add_field(name = 'Права:', value = '`Банить участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`unban`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`un-ban [айди участника] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`un-mute 614424106242277416`\n`un-ban 614424106242277416 ошибочный бан`', inline = False)
			emb.add_field(name = 'Права:', value = '`Банить участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`unban`', inline = False)
			await ctx.send(embed = emb)


	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`ban [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`ban @участник`\n`ban @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Банить участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`ban`, `b`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`ban [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`ban @участник`\n`ban @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Банить участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`ban`, `b`', inline = False)
			await ctx.send(embed = emb)


	@tempban.error
	async def tempban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\nПримеры формата времени: `1s`, `1m`, `1h`, `1d`',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`temp-ban [@участник] [время] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`temp-ban @участник 1h`\n`temp-ban @участник 2d нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Банить участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`tempban`, `t-ban`, `tb`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`temp-ban [@участник] [время] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`temp-ban @участник 1h`\n`temp-ban @участник 2d нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Банить участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`tempban`, `t-ban`, `tb`', inline = False)
			await ctx.send(embed = emb)


	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`kick [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`kick @участник`\n`kick @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Выгонять участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`kick`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`kick [@участник] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`kick @участник`\n`kick @участник нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Выгонять участников`, `Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`kick`', inline = False)
			await ctx.send(embed = emb)


	@modrole.error
	async def modrole_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mod-role [enable/disable] (@роль)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mod-role enable @модератор`\n`mod-role disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`modrole`, ``', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`modrole [enable/disable] (@роль)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`modrole enable @модератор`\n`modrole disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`modrole`', inline = False)
			await ctx.send(embed = emb)

	@muterole.error
	async def muterole_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mute-role [enable/disable] (@роль)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mute-role enable @мут`\n`mute-role disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`muterole`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mute-role [enable/disable] (@роль)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mute-role enable @роль`\n`mute-role disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`muterole`', inline = False)
			await ctx.send(embed = emb)


	@modlog.error
	async def modlog_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mod-log [enable/disable] (#канал)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mod-log enable #логи-модерации`\n`mod-log disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`modlog`, `m-log`, `ml`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mod-log [enable/disable] (#канал)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mod-log enable #логи-модерации`\n`mod-log disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`modlog`, `m-log`, `ml`', inline = False)
			await ctx.send(embed = emb)


	@tempmute.error
	async def tempmute_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\nПримеры формата времени: `1s`, `1m`, `1h`, `1d`',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`temp-mute [@участник] [время] (причина)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`temp-mute @участник 1h`\n`temp-mute @участник 1d нарушение правил`', inline = False)
			emb.add_field(name = 'Права:', value = '`Модератор`,`Администратор`,`Создатель сервера`')
			emb.add_field(name = 'Псевдонимы:', value = '`tempmute`, `t-mute`, `tm`', inline = False)
			await ctx.send(embed = emb)

	@massrole.error
	async def massrole_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mass-role [add/remove] [@цель] [@роль]`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mass-role @everyone @новобранец`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`,`Создатель сервера`')
			emb.add_field(name = 'Псевдонимы:', value = '`massrole`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`mass-role [add/remove] [@цель] [@роль]`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`mass-role @everyone @новобранец`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`,`Создатель сервера`')
			emb.add_field(name = 'Псевдонимы:', value = '`massrole`', inline = False)
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(moderation(bot))
	print ('[LOGS]: библиотека MODERATION успешно загружена.')