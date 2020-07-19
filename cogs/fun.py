import discord
import nekos
import random
import asyncio
import time
from discord.ext import commands

class fun (commands.Cog):
	def __init__(self, bot):
		self.Bot = bot


	@commands.command()
	async def hug(self, ctx, member : discord.Member = None):
		if member == None:
			emb = discord.Embed(
				description= f'{ctx.author.mention} обнял(а) всех'
    		)
			emb.set_image(url=nekos.img('hug'))
			await ctx.send(embed = emb)
		else:
			if member == ctx.message.author:
				await ctx.send('<:xmark:731024248222777374>Вы не можете обнять сами себя.')
			else:
				emb = discord.Embed(
    			description= f'{member.mention}, Вас обнял(а) {ctx.author.mention}.'
    			)
				emb.set_image(url=nekos.img('hug'))

				await ctx.send(embed=emb)

	@commands.command()
	async def slap(self, ctx, member : discord.Member = None):
		if member == None:
			emb = discord.Embed(
				description= f'{ctx.author.mention} ударил(а) всех'
    			)
			emb.set_image(url=nekos.img('slap'))
			await ctx.send(embed = emb)
		else:
			if member == ctx.message.author:
				await ctx.send('<:xmark:731024248222777374>Вы не можете ударить сами себя.')
			else:
				emb = discord.Embed(
				description= f'{member.mention}, Вас ударил(а) {ctx.author.mention}.'
				)
        
				emb.set_image(url=nekos.img('slap'))
 
				await ctx.send(embed=emb)


	@commands.command()
	async def pat(self, ctx, member : discord.Member = None):
		if member == None:
			emb = discord.Embed(
				description= f'{ctx.author.mention} погладил(а) всех'
    			)
			emb.set_image(url=nekos.img('pat'))
			await ctx.send(embed = emb)

		else:
			if member == ctx.message.author:
				await ctx.send('<:xmark:731024248222777374>Вы не можете погладить сами себя.')
			else:
				emb = discord.Embed(
				description= f'{member.mention}, Вас погладил(а) {ctx.author.mention}.'
				)

				emb.set_image(url=nekos.img('pat'))
 
				await ctx.send(embed=emb)


	@commands.command()
	async def kiss(self, ctx, member : discord.Member = None):
		if member == None:
			emb = discord.Embed(
				description= f'{ctx.author.mention} поцеловал(а) всех'
    			)
			emb.set_image(url=nekos.img('kiss'))
			await ctx.send(embed = emb)

		else:
			if member == ctx.message.author:
				await ctx.send('<:xmark:731024248222777374>Вы не можете поцеловать сами себя.')
			else:
				emb = discord.Embed(
				description= f'{member.mention}, Вас поцеловал(а) {ctx.author.mention}.'
					)
        
				emb.set_image(url=nekos.img('kiss'))

				await ctx.send(embed=emb)


	@commands.command()
	async def tickle(self, ctx, member : discord.Member = None):
		if member == None:
			emb = discord.Embed(
				description= f'{ctx.author.mention} пощекотал(а) всех'
    			)
			emb.set_image(url=nekos.img('tickle'))
			await ctx.send(embed = emb)

		else:
			if member == ctx.message.author:
				await ctx.send('<:xmark:731024248222777374>Вы не можете пощекотать самого себя.')
			else:
				emb = discord.Embed(
				description= f'{member.mention}, Вас пощекотал(а) {ctx.author.mention}.'
				)
        
				emb.set_image(url=nekos.img('tickle'))

				await ctx.send(embed=emb)
				

	@commands.command()
	async def monetka(self, ctx, arg = None):
		monetka = ['Орёл', 'Решка']
		orel = ['Орёл', 'орёл']
		reshka = ['Решка', 'решка']
		cva = random.choice(monetka)
		if arg in reshka:
			emb = discord.Embed(
				description = f'**Вы угадалии, вам выпала** ``{cva}``!',
				colour = discord.Colour.green()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			msg = await ctx.send('**Вы выбрали ``решка``, подкидываем монетку...**')
			await asyncio.sleep(3)
			if cva =='Решка':
				await msg.edit(content = None, embed = emb)
			else:
				embed = discord.Embed(
					description = f'**Вы не угадали, выпал ``{cva}``**',
					colour = discord.Colour.red()
					)
				embed.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				await msg.edit(content = None, embed = embed)

		elif arg in orel:
			emb = discord.Embed(
				description = f'**Вы угадали, вам выпал** ``{cva}``!',
				colour = discord.Colour.green()
				)
			emb.set_author(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			msg = await ctx.send('**Вы выбрали ``Орёл``, подкидываем монетку...**')
			await asyncio.sleep(3)
			if cva=='Орёл':
				await msg.edit(content = None, embed = emb)
			else:
				embed = discord.Embed(
					description = f'**Вы не угадали, выпала ``{cva}``**',
					colour = discord.Colour.red()
					)
				embed.set_author(
					name = f'{ctx.author.name}#{ctx.author.discriminator}',
					icon_url = ctx.author.avatar_url
					)
				await msg.edit(content = None, embed = embed)
		else:
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите правильно все аргументы!**\n\n**Использовать:**\n``monetka [Решка/Орёл]``',
				colour = discord.Colour.red()
				)
			emb.set_footer(
				name = f'{ctx.author.name}#{ctx.author.discriminator}',
				icon_url = ctx.author.avatar_url
				)
			await ctx.send(embed = emb)


	@monetka.error
	async def monetka_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(
				description = '**<:xmark:731024248222777374>Введите все аргументы!**',
				colour = discord.Colour.red()
				)
			emb.add_field(name = 'Использовать:', value = '`monetka [орёл/решка]`', inline = False)
			emb.add_field(name = 'Примеры:', value = '`monetka орёл`\n`monetka решка`', inline = False)
			emb.add_field(name = 'Права:', value = '`Участник`')
			emb.add_field(name = 'Псевдонимы:', value = '`monetka`', inline = False)
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(fun(bot))
	print('[LOGS]: библиотека FUN успешно загружена.')