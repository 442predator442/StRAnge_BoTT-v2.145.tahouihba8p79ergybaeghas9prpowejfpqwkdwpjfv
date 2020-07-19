import discord
from discord.ext import commands
import time
import requests
import asyncio
import os
import datetime
from datetime import timedelta


class info(commands.Cog):
	def __init__(self, bot):
		self.Bot = bot


	@commands.command(aliases = ['server-info','server'])
	async def serverinfo(self, ctx):
		member = ctx.guild.members
		roles = len(ctx.guild.roles)
		members = len(ctx.guild.members)
		channels = len(ctx.guild.channels)
		text_channels = len(ctx.guild.text_channels)
		voice_channels = len(ctx.guild.voice_channels)
		emojis = len(ctx.guild.emojis)
		online = len(list(filter(lambda x: x.status == discord.Status.online, member)))
		idle = len(list(filter(lambda x: x.status == discord.Status.idle, member)))
		dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, member)))
		offline = len(list(filter(lambda x: x.status == discord.Status.offline, member)))
		verification = ctx.message.guild.verification_level
		if verification ==discord.VerificationLevel.none:
			verification = 'Отсутствует'
		elif verification ==discord.VerificationLevel.low:
			verification = 'Слабая'
		elif verification ==discord.VerificationLevel.medium:
			verification = 'Средняя'
		elif verification ==discord.VerificationLevel.high:
			verification = 'Высокая'
		elif verification ==discord.VerificationLevel.extreme:
			verification = 'Очень высокая'


		emb = discord.Embed(
			colour = ctx.message.author.colour
			)
		emb.add_field(name = 'Айди сервера', value = f'{ctx.message.guild.id}')
		emb.add_field(name = 'Владелец', value = ctx.message.guild.owner.mention)
		emb.add_field(name = f'Участников[{members}]', value = f'<:online:730816375332798496>{online} онлайн\n<:idle:730817053325262948>{idle} не активен\n<:dnd:730817459245940848>{dnd} не беспокоить\n<:offline:730816392630239332>{offline} оффлайн', inline = False)
		emb.add_field(name = f'Каналы[{channels}]', value = f'<:textchannel:730815659734204457> {text_channels} текстовых<:space:730818398199480342><:voicechannel:730816361697116281>{voice_channels} голосовых', inline = False)
		emb.add_field(name = 'Ролей', value = roles)
		emb.add_field(name = 'Эмодзи', value = emojis)
		emb.add_field(name = 'Уровень верификации', value = verification, inline = False)
		emb.add_field(name = 'Был создан', value = f'{ctx.message.guild.created_at.strftime("%d.%m.%Y | %H:%M:%S")}')
		emb.set_author(
			name = ctx.message.guild.name
			)
		emb.set_thumbnail(url = ctx.message.guild.icon_url)
		await ctx.send(embed = emb)


	@commands.command()
	async def user(self, ctx, member: discord.Member = None):
		user = ctx.message.author if member == None else member
		mob = user.is_on_mobile()

		if user.status ==discord.Status.offline:
			mob ='Не известно'

		elif mob == True:
			mob ='Мобильное устройство'

		elif mob == False:
			mob ='ПК'
		status = user.status
		if status == discord.Status.online:
			status ='<:online:730816375332798496>В сети'
		elif status == discord.Status.idle:
			status ='<:idle:730817053325262948>Не активен'
		elif status == discord.Status.offline:
			status ='<:offline:730816392630239332>Оффлайн'
		elif status == discord.Status.invisible:
			status ='<:offline:730816392630239332>Невидимка'
		elif status == discord.Status.dnd:
			status ='<:dnd:730817459245940848>Не беспокоить'
		emb = discord.Embed(
			title = f'{user.name}#{user.discriminator}',
			colour = user.colour
			)
		emb.add_field(name = 'Ник:', value = f'{user.display_name}')
		emb.add_field(name = 'Айди:', value = f'{user.id}')
		emb.add_field(name = 'Статус:', value = f'{status}', inline = False)
		emb.add_field(name = 'Цвет:', value = f'{user.colour}', inline = False)
		emb.add_field(name = 'Создал аккаунт:', value = f'{user.created_at.strftime("%d.%m.%Y %H:%M:%S")}')
		emb.add_field(name = 'Приесоденился на сервер:', value = f'{user.joined_at.strftime("%d.%m.%Y %H:%M:%S")}')
		emb.add_field(name = 'Устройство:', value = f'{mob}', inline = False)
		emb.add_field(name = 'Высшая роль:', value = f'{user.top_role}')
		emb.add_field(name = 'Количество ролей:', value = f'{len(user.roles)}', inline = False)
		emb.set_thumbnail(url = user.avatar_url)
		await ctx.send(embed = emb)


	@commands.command() 
	async def activity(self, ctx, channel: discord.TextChannel = None):
		if not channel:
			channel = ctx.channel
			text = 'в этом канале'
		else:
			text = f'в #{channel.id}'
		msg = await ctx.send('**Начинаю вычисление...**')
		counter = 0
		yesterday = datetime.datetime.today() - timedelta(days = 1)
		async for message in channel.history(limit=None, after=yesterday):
			counter += 1
		counter2 = 0
		weekago = datetime.datetime.today() - timedelta(weeks = 1)
		async for message in channel.history(limit=None, after=weekago):
			counter2 += 1
		counter3 = 0
		monthago = datetime.datetime.today() - timedelta(weeks = 4)
		async for message in channel.history(limit=None, after=monthago):
			counter3 += 1
		embed = discord.Embed(title = f'Статиститка сообщений {text}')
		embed.add_field(name = 'За сегодня:', value = f'{counter}', inline = False)
		embed.add_field(name = 'За неделю:', value = f'{counter2}', inline = False) 
		embed.add_field(name = 'За месяц:', value = f'{counter3}', inline = False) 
		embed.set_author(
			name = f'{ctx.author.name}#{ctx.author.discriminator}',
			icon_url = ctx.author.avatar_url
			)
		embed.set_footer(text = f'Канал: #{channel}')
		await msg.edit(content = None, embed = embed)


def setup(bot):
	bot.add_cog(info(bot))
	print('[LOGS]: библиотека INFO успешно загружена.')