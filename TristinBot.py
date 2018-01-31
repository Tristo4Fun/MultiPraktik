import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import secrets
from lxml import html
import requests
from imgurpython import ImgurClient
import praw

#initialising Reddit user
reddit = praw.Reddit(client_id='v3db9YiZJ4C6Qg',client_secret='XLaHy5KZKAWXkg87ZIAXI5AzcVI',user_agent='aeaeae')

#initialising Imgur user
imgclient_id = '97b71b83dba9104'
imgclient_secret = 'ea5c168dc44c9af8f82ed23ab07481a992da28a3'
imgclient = ImgurClient(imgclient_id, imgclient_secret)


client = Bot(description="Najbolji bot north of the wall", command_prefix="!", pm_help = False, )
@client.event
async def on_ready():
	print("Bot is ready!")
	return await client.change_presence(game=discord.Game(name='Still being developed'))
# async def on_message(message):
# 	new = ""
# 	for s in message.content:
# 		new+=s
# 	if "who" in message.content and "am" in message.content and "i" in message.content:
# 		await client.send_message(message.channel,message.author)

@client.command()
async def plagius(*args):
	file = open("plagius.txt", "r")
	for line in file:
		await client.say(line)
	file.close()
	print("Plagius the wise by {}".format(client.user.name))

@client.command()
async def random(*args):
	await client.say(secrets.choice(args))

@client.command()
async def quote(*args):
	lines = open('quote.txt').read().splitlines()
	await client.say(secrets.choice(lines))
	print("Quote printed by {}".format(client.user.name))

@client.command(pass_context = True)
async def dab(ctx, *args):
    #await client.delete_message(ctx.message)
    await client.say(":trumpet: :trumpet: :trumpet: *dabs* :trumpet: :trumpet: :trumpet: :trumpet: ")

@client.command(pass_context = True)
async def hype(ctx,*args):
	await client.delete_message(ctx.message)
	await client.say("WOOOOOOOOOOOOOOOOOOOOOOOOO LET'S FUCKING GOOOOOOOOOOOOOO")

@client.command(pass_context = True)
async def killhype(ctx,*args):
	await client.delete_message(ctx.message)
	await client.say("fuck this game")

@client.command()
async def clap(*args):
	new = ""
	for arg in args:
		new+=arg + ":clap::skin-tone-4:"
	await client.say(new)

@client.command()
async def stats(*args):
	print(args[0])
	name = args[0]
	#if it doesn't work make a string first
	url = 'https://csgo-stats.com/search/'+name
	page = requests.get(url)
	print(url)
	tree = html.fromstring(page.content)
	statistics = tree.xpath('//span[@class="main-stats-data-row-data"]/text()')
	#stats2= tree.xpath('//div[@class="stats-row"]/text()')
	#await client.say(prices)
	endstring = ""
	endstring+="Kills:  "
	endstring+=statistics[0]
	endstring+="\nTime played:  "
	endstring+=statistics[1]
	endstring+="\nWin %:  "
	endstring+=statistics[2]
	endstring+="\nAccuracy:  "
	endstring+=statistics[3]
	endstring+="\nHeadshot %:  "
	endstring+=statistics[4]
	endstring+="\nMVPs:  "
	endstring+=statistics[5]
	await client.say(endstring)


@client.command()
async def pic():
	items = imgclient.gallery_random(section='hot', sort='viral', page=0, window='day', show_viral=True)
	await client.say(items.link)

@client.command()
async def meme():
	items = imgclient.memes_subgallery(sort='best', page=0, window='day')
	await client.say(secrets.choice(items).link)


@client.command()
async def red(*args):
	show = True
	lines = open('nsfw.txt').read().splitlines()
	for line in lines:
		if args[0] == line:
			show = False
	if show == True:
		posts = reddit.subreddit(args[0]).hot(limit=30)
		random_post_number = secrets.randbelow(30)
		for i,post in enumerate(posts):
			if i==random_post_number:
				await client.say(post.title)
				await client.say(post.url)
	elif show == False:
		await client.say("c-c-c, shame on u")

@client.command()
async def risky():
	lines = open('nsfw.txt').read().splitlines()
	line = secrets.choice(lines)
	posts = reddit.subreddit(line).hot(limit=30)
	random_post_number = secrets.randbelow(30)
	for i,post in enumerate(posts):
		if i==random_post_number:
			await client.send_message(client.get_channel('407188548220092426'),post.title)
			await client.send_message(client.get_channel('407188548220092426'),post.url)


@client.command(pass_context = True)
async def game(ctx,*args):
	msg = "Hey @everyone let's play some "
	for arg in args:
		msg += arg
		msg += " "
	await client.delete_message(ctx.message)
	await client.say(msg)

@client.command()
async def twitch(*args):
	strm = "https://www.twitch.tv/"+ args[0]
	await client.say(strm)

@client.event
async def on_message(message):
	if message.content.startswith('$greet'):
		msg = await client.send_message(message.channel, 'React with thumbs up or thumbs down.')
		res = await client.wait_for_reaction(['👍', '👎'], message=msg)
		await client.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))

#hangman
@client.event
async def on_message(message):
	if message.content.startswith('!hang'):
		lost = False
		hangboy = 0
		done = False
		lines = open('hang.txt').read().splitlines()
		word = secrets.choice(lines)
		await client.send_message(message.channel,"word: {}".format(word))
		mistery = ""
		for c in word:
			mistery += "-"
			mistery += " "
		print(mistery)
		mist = mistery.split()
		await client.send_message(message.channel," ".join(mist))
		ongoing = True
		while(ongoing):
			def check(msg):
				return msg.content.startswith('$guess')

			message = await client.wait_for_message(author=message.author, check=check)
			letter = message.content[len('$guess'):].strip()
			print(mist)
			await client.send_message(message.channel,letter)
			if letter in word:
				mist[word.index(letter)] = letter
				word = list(word)
				print(word)
				word[word.index(letter)] = "-"
				word = "".join(word)
				await client.send_message(message.channel, '{} is cool indeed'.format(letter))
			else:
				hangboy +=1
				await client.send_message(message.channel, '{} is a no my dude'.format(letter))
			print(hangboy)
			if "-" in mist:
				ongoing = True
				done = False
			else:
				ongoing = False
				done = True
			if (hangboy > 4):
				lost = True
				ongoing = False
		if done == True:
			print(mist)
			await client.send_message(message.channel,":trophy: Congratulations :trophy:")
		if lost == True:
			print(mist)
			await client.send_message(message.channel,"Better luck next time!")
	await client.process_commands(message)
# @client.command(pass_context = True)
# async def game(ctx,*args):
client.run('NDA1MDUzMDgxOTk5NjM4NTI5.DUf0dA.DGPj48lv23Gk5z0lYqzzYi87z3k')
#  @client.command()
# async def bye(*args):
# 	Application.Start(yourexename.exe);
# 	await discord.Disconnect();


#SLEEP WAIT PAUSE
#await asyncio.sleep(3)
