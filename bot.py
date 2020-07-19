import discord
import asyncio
import os
from discord.ext import commands
from discord.ext.commands import Bot
import time
from random import randint
import requests
from discord import Webhook, RequestsWebhookAdapter
import wikipedia
import nekos
import sqlite3
import datetime
from datetime import timedelta

default_prefix = '.'

sqlite_pref = 'db/Prefix.db'
db = sqlite3.connect(sqlite_pref)
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS prefix(
	pref varchar(20),
	guildid BIGINT)""")
db.commit()
db.close()


async def determine_prefix(bot, message):
	if not message.channel.type in [discord.ChannelType.text, discord.ChannelType.news, discord.ChannelType.store]:
		return default_prefix
	else:
		db = sqlite3.connect(sqlite_pref)
		cursor = db.cursor()
		cursor.execute(f"SELECT pref FROM prefix WHERE guildid='{message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			return default_prefix
		else:
			preff = res[0][0]
			return preff
		db.commit()
		db.close()


bot = commands.Bot(command_prefix = determine_prefix)
bot.remove_command('help')


for file in os.listdir('./cogs'):
	if file.endswith('.py'):
		bot.load_extension(f'cogs.{file[:-3]}')

sqlite_log = 'db/Logs.db'
db = sqlite3.connect(sqlite_log)
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS log(
	lchannel BIGINT,
	guildid BIGINT)""")
db.commit()
db.close()


@bot.event
async def on_command_error(ctx, error):
	pass


@bot.event
async def on_member_join(member):
	if member.guild.id == 664742836624818176:
		members = len(member.guild.members)
		guild = member.guild
		channel = discord.utils.find (lambda c: c.id ==670666494182555662, guild.text_channels)
		ochannel = discord.utils.find(lambda c: c.id ==690315598399406212, guild.text_channels)
		emb = discord.Embed(title = f'{guild.name}', description = f'У нас новенький(-ая), {member.mention}\n\n\n**[📋] Узнать все доступные команды сервера** - ``.help``\n\n\n**[📜] Ознакомится с правилами ты сможешь здесь** - \n<#690315259944501519>\n\n**[🐍] Научится создавать бота** - <#719806592534708254>', colour = discord.Colour.green())
		emb.set_author(name = f'{member.name}', icon_url = member.avatar_url)
		emb.set_image (url = 'https://i.gifer.com/8CPR.gif')
		e = discord.Embed(
			description = f'**<:check:731024265826140311>У нас новенький(-ая), {member.mention}!**\nПриветствуем тебя на сервер ``{member.guild.name}!``\nНе забудь ознакомится с правилами - <#690315259944501519>\n**На нашем сервере уже {members} участников!**',
			colour = discord.Colour.blue()
			)
		await channel.send(embed = emb)
		await ochannel.send(embed = e)

		new_role = discord.utils.get(member.guild.roles, name = '〘🔑〙Verific')
		await member.add_roles(new_role)
	else:
		pass


@bot.event
async def on_message_delete(message):
	if message.author.bot:
		return
	else:
		db = sqlite3.connect(sqlite_log)
		cursor = db.cursor()
		cursor.execute(f"SELECT lchannel FROM log WHERE guildid='{message.guild.id}'")
		res = cursor.fetchall()
		for i in cursor.execute(f"SELECT lchannel FROM log WHERE guildid='{message.guild.id}'"):
			logs = i[0]
			log = message.guild.get_channel(logs)

		if not res:
			return

		else:
			for attachment in message.attachments:
					if attachment.filename.endswith(('.bmp', '.jpeg', '.jpg', '.png', '.gif')):
						file = message.attachments[0].url
						embed = discord.Embed(
							title = '🚮Message Deleted', 
							description = f'**User:** {message.author.mention}\n**Channel:** <#{message.channel.id}>\n**Message**: {file}', 
							colour = discord.Colour.red()
							)
						await log.send(embed = embed)
						return

			if message.content == str or int:
				emb = discord.Embed(title = '🚮Message Deleted', description = f'**User:** {message.author.mention}\n**Channel:** <#{message.channel.id}>\n**Message**: {message.content}', colour = discord.Colour.red())
				emb.set_footer(text = f'Message ID: {message.id}')
				await log.send(embed = emb)
		db.close()




@bot.event
async def on_message_edit(msg_b, msg_a):
	if msg_b.author.bot:
		return
	await bot.process_commands(msg_a)
	db = sqlite3.connect(sqlite_log)
	cursor = db.cursor()
	cursor.execute(f"SELECT lchannel FROM log WHERE guildid='{msg_b.guild.id}'")
	res = cursor.fetchall()
	if not res:
		return

	else:
		for i in cursor.execute(f"SELECT lchannel FROM log WHERE guildid='{msg_b.guild.id}'"):
			logs = i[0]
			log = msg_b.guild.get_channel(logs)

			emb = discord.Embed(title = '📝Edit Message', description = f'**User:** {msg_b.author.mention}\n**Channel:** <#{msg_b.channel.id}>\n\n**Before message:** {msg_b.content}\n\n**After message:** {msg_a.content}', colour = discord.Colour.gold())
			emb.set_footer(text = f'Message ID: {msg_b.id}')
			await log.send(embed = emb)
			return
	db.close()


@bot.event
async def on_member_remove(member):
	if member.guild.id == 664742836624818176:
		guild = member.guild
		channel = discord.utils.find (lambda c: c.id ==670666605440794654, guild.text_channels)
		emb = discord.Embed(title = f'**{member.name}#{member.discriminator}** покинул наш сервер👋', colour = discord.Colour.red())
		emb.set_image(url = 'https://media.giphy.com/media/9eM1SWnqjrc40/giphy.gif')
		await channel.send(embed = emb)

	else:
		pass


@bot.event
async def on_ready():
    print ("Странный Бот подключился!")
    await bot.change_presence( status = discord.Status.online)


@bot.event
async def on_message(message):
	await bot.process_commands(message)


@bot.command()
async def help(ctx):

	msg = await ctx.send('**Подождите...**')

	await msg.add_reaction('📁')
	await msg.add_reaction('🔨')
	await msg.add_reaction('🔧')
	await msg.add_reaction('📃')
	await msg.add_reaction('🖱')

	await asyncio.sleep(1)

	await msg.edit(content = '***<:check:731024265826140311>Выбери категорию:***\n\n📁 - **General**\n🔨 - **Moderation**\n🔧 - **Config**\n📃 - **Info**\n🖱 - **Games and fun**')

	r_list = ['📁', '🔧', '🔨', '📃', '🖱']

	try:
		reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in r_list)

	except:
		pass

	else:
		if str(reaction.emoji) == '📁':
			emb = discord.Embed(
				title = 'Команды по умолчанию:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``avatar (@участник)``\nВывод твоей аватарки или упомянутого участника.\n\n``suggest [идея]``\nОтправка твоей идеи для сервера.\n\n``ping``\nПинг бота.',
				colour = discord.Colour.dark_blue()
				)

			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('🔨')
			await msg.clear_reaction('📁')

			await msg.add_reaction('<:check:731024265826140311>')
			e_list = ['<:check:731024265826140311>']

			try:
				reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except:
				pass

			else:
				if str(reaction.emoji) == '<:check:731024265826140311>':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


		elif str(reaction.emoji) == '🔨':
			emb = discord.Embed(
				title = 'Команды для модерации:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``clear [к-во]``\nОчистить заданое количество сообщений.\n\n``warn [@участник] (причина)``\nВыдать предуприждение упомянутому участнику.\n\n``mute [@участник] (причина)``\nВыдать навсегда мут упомянутому участнику.\n\n``tempmute [@участник] [время] (причина)``\nВыдать мут упомянутому участнику на заданное время.\n\n``un-mute [@участник] (причина)``\nСнять ограничения(мут) с упомянутого участника.\n\n``kick [@участник] (причина)``\nВыгнать упомянутого участника.\n\n``ban [@участник] (причина)``\nЗабанить упомянутого участника.\n\n``temp-ban [@участник] [время] (причина)``\nЗабанить упомянутого участника на заданное время.\n\n``un-ban [айди участника] (причина)``\nРозбанить указаного участника\n\n``ban-list``\nСписок забаненных участников.\n\n``mass-role [add/remove] [@цель] [@роль]``\nВыдать или удалить роль с участников, имеющие указанную роль(@цель).',
				colour = discord.Colour.dark_blue()
				)

			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('🔨')
			await msg.clear_reaction('📁')

			await msg.add_reaction('<:check:731024265826140311>')
			e_list = ['<:check:731024265826140311>']

			try:
				reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except:
				pass

			else:
				if str(reaction.emoji) == '<:check:731024265826140311>':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)

		elif str(reaction.emoji) == '🔧':
			emb = discord.Embed(
				title = 'Команды для настройки сервера (конфиг):',
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n```Префикс:```\n``.prefix (префикс)``\nЗадать префикс бота или узнать текущий префикс.\n\n```Система идей:```\n``suggestions [enable/disable] (#канал_для_идей)``\nПодключить или отключить систему идей.\n\n```Система новостей:```\n``news-channel [enable/disable] (#канал_новостей)``\nПодключить или отключить систему новостей.\n\n```Система верификации```\n``verific-role [enable/disable] (@роль)``\nУказать или сбросить роль верификации, тем самым подключая или выключая систему верификации.\n\n```Система логов:```\n``chat-log [enable/disable] [#канал_логов]``\nПодключить или отключить чат логи.\n\n``mod-log [enable/disable] (#канал_логов)``\nПодключить или отключить логи модерации.\n\n```Конфиг модерации:```\n``mod-role [enable/disable] [@роль]``\nУказать или сбросить роль модератора.\n\n``mute-role [enable/disable] (@роль)``\nУказать или сбросить мут-роль.',
				colour = discord.Colour.dark_blue()
				)

			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('🔨')
			await msg.clear_reaction('📁')

			await msg.add_reaction('<:check:731024265826140311>')
			e_list = ['<:check:731024265826140311>']

			try:
				reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except:
				pass

			else:
				if str(reaction.emoji) == '<:check:731024265826140311>':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)



		elif str(reaction.emoji) == '📃':
			emb = discord.Embed(
				title = 'Инфо:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``help``\nПомощь по коммандам.\n\n``server-info``\nИнформация о сервере.\n\n``user (@участник)``\nИнформация о тебе или об указанном участнике.\n\n``bot-info``\nИнформация о боте.\n\n``server-count``\nУзнать количество серверов, на котором находится бот.\n\n``activity (#канал)``\n**Информация о активе канала.**', 
				colour = discord.Colour.dark_blue()
				)

			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('🔨')
			await msg.clear_reaction('📁')

			await msg.add_reaction('<:check:731024265826140311>')
			e_list = ['<:check:731024265826140311>']

			try:
				reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except:
				pass

			else:
				if str(reaction.emoji) == '<:check:731024265826140311>':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


		elif str(reaction.emoji) == '🖱':
			emb = discord.Embed(
				title = 'Игры и веселье:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``hug``\nОбнять упомянутого участника.\n\n``slap``\nУдарить упомянутого участника.\n\n``pat``\nПогладить упомянутого участника.\n\n``kiss``\nПоцеловать упомянутого участника.\n\n``tickle``\nПощекотать упомянутого участника.\n\n``monetka [Орёл/Решка]``\nБросить монетку (Орёл или Решка).\n\n``ttt [@участник]``\nПредложить игру "Крестики-Нолики" указаному участнику.', 
				colour = discord.Colour.dark_blue()
				)

			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('🔨')
			await msg.clear_reaction('📁')

			await msg.add_reaction('<:check:731024265826140311>')
			e_list = ['<:check:731024265826140311>']

			try:
				reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except:
				pass

			else:
				if str(reaction.emoji) == '<:check:731024265826140311>':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


@bot.command(aliases = ['bot-info'])
async def botinfo(ctx):
	emb = discord.Embed(
		description = '===============================================\n\n╔ **Создатель бота:** <@614424106242277416>\n║\n╠ **Сервер бота:** временно отсутствует...\n║\n╠ **Сервер создателя:** https://discord.gg/baZUze6\n║\n╚ **Приглашение бота:** https://discord.com/api/oauth2/authorize?client_id=715848430345388043&permissions=8&scope=bot\n\n===============================================',
		colour = discord.Colour.green()
		)
	await ctx.send(embed = emb)


@bot.command()
async def ping(ctx): 
	emb = discord.Embed(
		description= f'**Пинг:** ``{bot.ws.latency * 1000:.0f} ms``',
		colour = 0x00ff00
		)
	await ctx.send(embed=emb)


@bot.command(aliases = ['server-count'])
async def servercount(ctx):
	emb = discord.Embed(
		description = f'**<:check:731024265826140311>Бот присутствует на {len(bot.guilds)} серверах.**',
		colour = discord.Colour.green()
		)
	emb.set_author(
		name = f'{ctx.author.name}#{ctx.author.discriminator}',
		icon_url = ctx.author.avatar_url
		)
	await ctx.send(embed = emb)


@bot.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *, arg):
	await ctx.message.delete()
	await ctx.send(arg)


@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx, pref = None):
	db = sqlite3.connect(sqlite_pref)
	cursor = db.cursor()
	cursor.execute(f"SELECT pref FROM prefix WHERE guildid='{ctx.message.guild.id}'")
	res = cursor.fetchall()
	if pref == None:
		if not res:
			await ctx.send(f'**На этом сервере установлен префикс по умолчанию** - `.`')
		else:
			for i in cursor.execute(f"SELECT pref FROM prefix WHERE guildid='{ctx.message.guild.id}'"):
				prefix = i[0]
				emb = discord.Embed(
					description = f'**Префикс бота** - `{prefix}`',
					colour = discord.Colour.green()
					)
				emb.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.message.author.avatar_url
					)
				await ctx.send(embed = emb)
	else:
		if not res:
			cursor.execute(f"INSERT INTO prefix VALUES('{pref}','{ctx.message.guild.id}')")
			db.commit()
			await ctx.send(f'***<:check:731024265826140311>Префикс `{pref}` успешно установлен***')
		else:
			cursor.execute(f"UPDATE prefix SET pref='{pref}' WHERE guildid='{ctx.message.guild.id}'")
			db.commit()
			await ctx.send(f'***<:check:731024265826140311>Префикс `{pref}` успешно установлен***')
	db.close()

	
@bot.command(aliases = ['chat-log','c-log'])
@commands.has_permissions(administrator = True)
async def chatlog(ctx, arg:str, channel: discord.TextChannel = None):
	db = sqlite3.connect(sqlite_log)
	cursor = db.cursor()
	cursor.execute(f"SELECT lchannel FROM log WHERE guildid='{ctx.message.guild.id}'")
	res = cursor.fetchall()

	if arg =='enable':
		if not res:
			cursor.execute(f"INSERT INTO log VALUES('{channel.id}','{ctx.message.guild.id}')")
			db.commit()
			await ctx.send('***<:check:731024265826140311>Канал чат-логов успешно установлен***')

		elif channel == None:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\n**Использовать:**\n``chat-log [enable/disable] (#канал_логов)``',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)

		else:
			cursor.execute(f"UPDATE log SET lchannel='{channel.id}' WHERE guildid='{ctx.message.guild.id}'")
			db.commit()
			await ctx.send('***<:check:731024265826140311>Канал чат-логов успешно обновлен***')

	elif arg == 'disable':
		if channel == None:
			if not res:
				await ctx.send('***<:xmark:731024248222777374>На этом сервере уже отключены логи!***')
			else:
				cursor.execute(f"DELETE FROM log WHERE guildid='{ctx.message.guild.id}'")
				db.commit()
				await ctx.send('***<:check:731024265826140311>Чат-логи успешно отключены***')

		else:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**\n\n**Использовать:**\n``chat-log [enable/disable] (#канал_логов)``',
				colour = discord.Colour.red()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)
	db.close()


@bot.command()
async def verify(ctx):
	sqlite_verify = 'db/Verify.db'
	db = sqlite3.connect(sqlite_verify)
	cursor = db.cursor()
	cursor.execute(f"SELECT vrole FROM verole WHERE guildid='{ctx.message.guild.id}'")
	res = cursor.fetchall()
	if not res:
		await ctx.send('***<:xmark:731024248222777374>На этом сервере не указана роль верификации!***\n\n*Использовать:* ``verific-role [enable/disable] (@роль)``')
	else:
		for i in cursor.execute(f"SELECT vrole FROM verole WHERE guildid='{ctx.message.guild.id}'"):
			vr = i[0]
			vrole = ctx.guild.get_role(vr)
			roles = ctx.author.roles
			if vrole in roles:
				emb = discord.Embed(
					description = '**<:xmark:731024248222777374> Ваш аккаунт уже верифицирован!**',
					colour = discord.Colour.red()
					)
				emb.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				await ctx.send(embed = emb)

			else:
				emb = discord.Embed(
					description = '**Чтобы пройти верификацию, нажми на реакцию под этим сообщением.**',
					colour = discord.Colour.green()
					)
				msg = await ctx.send(embed = emb)
				await msg.add_reaction('<:check:731024265826140311>')
				rec_list =['<:check:731024265826140311>']

				try:
					reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in rec_list)
				except:
					pass
				else:
					if str(reaction.emoji) =='<:check:731024265826140311>':
						await ctx.message.author.add_roles(vrole)
						embed = discord.Embed(
							description = f'**<:check:731024265826140311> Вы успешно прошли верификацию на сервере ``{ctx.guild.name}``!**',
							colour = discord.Colour.green()
							)
						await user.send(embed = embed)
			
	db.close()


@chatlog.error
async def chatlog_error(ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`chat-log [enable/disable] (#канал)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`chat-log enable #логи-модерации`\n`chat-log disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`chatlog`, `c-log`', inline = False)
			await ctx.send(embed = emb)

		elif isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Недостаточно прав на использование данной команды!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`chat-log [enable/disable] (#канал)`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`chat-log enable #логи-модерации`\n`chat-log disable`', inline = False)
			emb.add_field(name = 'Права:', value = '`Администратор`, `Создатель сервера`', inline = False)
			emb.add_field(name = 'Псевдонимы:', value = '`chatlog`, `c-log`', inline = False)
			await ctx.send(embed = emb)


bot.run('NzE1ODQ4NDMwMzQ1Mzg4MDQz.XxQEFg.Zros6Xg4ZisxdY6zVgkccqH85BA')