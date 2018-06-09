import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import secrets
from lxml import html
import requests
from imgurpython import ImgurClient
import praw
import os
#reading channel info
ch = open('channels.txt').read().splitlines()
risk = ch[0]
retar = ch[1]
daily = ch[2]
#initialising Reddit user
reddit = praw.Reddit(client_id='v3db9YiZJ4C6Qg',client_secret='XLaHy5KZKAWXkg87ZIAXI5AzcVI',user_agent='aeaeae')

#initialising Imgur user
imgclient_id = '97b71b83dba9104'
imgclient_secret = 'ea5c168dc44c9af8f82ed23ab07481a992da28a3'
imgclient = ImgurClient(imgclient_id, imgclient_secret)

client = Bot(description="Najbolji bot north of the wall", command_prefix="!", pm_help = False, )

# @client.event
# async def my_background_task():
# 	print("yo")
# 	line = open('twitter.txt').read()
# 	with open('twitter.txt', 'w') as f:
# 		f.write('')
# 	if len(line)!=0:
# 		await client.send_message(client.get_channel('417039633122328606'),line)

async def my_background_task():
	await client.wait_until_ready()
	channel = discord.Object(id=daily)
	while not client.is_closed:
		line = open('twitter.txt').read()
		with open('twitter.txt', 'w') as f:
			f.write('')
		if len(line)!=0:
			await client.send_message(channel, line)
		await asyncio.sleep(5) # task runs every 60 seconds

@client.event
async def on_ready():

	print("Bot is ready!")
	
	return await client.change_presence(game=discord.Game(name='Still being developed'))
# async def on_message(message):
# 	new = ""
# 	for s in message.content:
#		new+=s
# 	if "who" in message.content and "am" in message.content and "i" in message.content:
# 		await client.send_message(message.channel,message.author)

@client.command()
async def plagius(*args):
	""" Writes Star Wars meme text. Syntax !plaguis """
	file = open("plagius.txt", "r")
	for line in file:
		await client.say(line)
	file.close()
	print("Plagius the wise by {}".format(client.user.name))

@client.command()
async def random(*args):
	""" Decides randomly from given words. Syntax !random word1 word2..."""
	await client.say(secrets.choice(args))

@client.command()
async def quote(*args):
	""" Gets random quote from somewhere. Syntax !quote """
	lines = open('quote.txt').read().splitlines()
	await client.say(secrets.choice(lines))
	print("Quote printed by {}".format(client.user.name))

@client.command(pass_context = True)
async def dab(ctx, *args):
	""" Makes the bot dab. Syntax: !dab """
    #await client.delete_message(ctx.message)
	await client.say(":trumpet: :trumpet: :trumpet: *dabs* :trumpet: :trumpet: :trumpet: :trumpet: ")

@client.command(pass_context = True)
async def hype(ctx,*args):
	""" Hypes you up. Syntax: !hype """
	await client.delete_message(ctx.message)
	await client.say("WOOOOOOOOOOOOOOOOOOOOOOOOO LET'S FUCKING GOOOOOOOOOOOOOO")

@client.command(pass_context = True)
async def killhype(ctx,*args):
	""" Kills hype. Syntax: !killhype """
	await client.delete_message(ctx.message)
	await client.say("fuck this game")

@client.command()
async def clap(*args):
	""" Turns message into meme. Syntax: !clap message """
	new = ""
	for arg in args:
		new+=arg + ":clap::skin-tone-4:"
	await client.say(new)

@client.command()
async def stats(*args):
	""" Gets CSGO stats from steamuser. Syntax: !stats steamName  """
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
	""" Gets random picture from imgur. Syntax !pic """
	items = imgclient.gallery_random(section='hot', sort='viral', page=0, window='day', show_viral=True)
	await client.say(items.link)

@client.command()
async def meme():
	""" Gets random meme from imgur. Syntax !meme """
	items = imgclient.memes_subgallery(sort='best', page=0, window='day')
	await client.say(secrets.choice(items).link)


@client.command()
async def red(*args):
	""" Gets a random post from a subreddit.Syntax: !red subredditName"""
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
	""" Random NSFW post from reddit. Syntax: !risky """
	lines = open('nsfw.txt').read().splitlines()
	line = secrets.choice(lines)
	posts = reddit.subreddit(line).hot(limit=30)
	random_post_number = secrets.randbelow(30)
	for i,post in enumerate(posts):
		if i==random_post_number:
			await client.send_message(client.get_channel(risk),post.title)
			await client.send_message(client.get_channel(risk),post.url)


@client.command(pass_context = True)
async def game(ctx,*args):
	""" Declares intention to play to @everyone. Syntax: !game nameOfGame"""
	print('{0.name} wrote '.format(ctx.message.author))
	print(args)
	msg = "Hey @everyone let's play some "
	for arg in args:
		msg += arg
		msg += " "
	await client.delete_message(ctx.message)
	await client.say(msg)

@client.command()
async def twitch(*args):
	""" Name of a twitch streamer into link. Syntax: !twitch streamerName"""
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
	""" Unfinished game of hangman. !hang random word, $guess"""
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
@client.command()
async def drop(ctx):
	""" Random drop location in PUBG/Fortnite. Syntax: !drop erangel/miramar/fortnite """
	erangel = ['Stalber','Woodcutters Camp','Gatka','Mansion','Zharki','School','Farm','Quarry','Prison','Pier Town','Hospital','Swamp town','Kameshki','Shelter','Yasnaya Polyana','Novorepnoye','Georgopol','Severny','Pochinki','Lipovka','Mylta Power','Primorsk','Shooting Range','Rozhok','Mylta','Military Base','Water Town','Ruins','Split (everyone has their own houses)','Crate Hunt (choose small drop near cars)']
	miramar=['Power Grind','San Martin','El Pozo','Ladrillera','Minas Generales','Torre Ahumada','Campo Militiar','Trailer Park','El Azahar','Impala','Ruins','Hacienda del Patron','Tierra Bronca','La Cobreria','Minas del Sur','La Bendita','Valle del Mar','Crater Fields','Puerto Paraiso','Minas del Valle','Water Treatment','Los Higos','Prison','Chumacera','Junkyard','Los Leones','Monte Nuevo','Pecado','Cruz del Valle','Graveyard''Split (everyone has their own houses)','Crate Hunt (choose small drop near cars)']
	fortnite=['Anarchy Acres','Fatal Fields','Flush Factory','Greasy Grove','Lonely Lodge','Loot Lake','Moisty Mire','Pleasant Park','Retail Row','Wailing Woods','Junk Junction','Haunted Hills','Tomato Town',
	'Tilted Towers','Snobby Shores','Salty Springs','Shifty Shafts','Dusty Depot','Motel','Pool','Right of Flush','Lucky Landing','Prison','CrateTown',]
	i=secrets.randbelow(len(erangel)-1)
	j=secrets.randbelow(len(miramar)-1)
	k=secrets.randbelow(len(fortnite)-1)
	if ctx.upper()=='MIRAMAR':
		await client.say('Drop at ' + miramar[j])
	elif ctx.upper()=='ERANGEL':
		await client.say('Drop at ' + erangel[i])
	elif ctx.upper()=='FORTNITE':
		await client.say('Drop at ' + fortnite[k])
	else:
		await client.say('... erangel ili miramar ili fortnite')

@client.command()
async def guard():
	""" Random quote from guards in Skyrim. Syntax : !guard """
	lines = open('skyrim1.txt').read().splitlines()
	line = secrets.choice(lines)
	left_text = line.partition("|")[0]
	#left_text = left_text.partition("[")[0]
	await client.say(left_text)

@client.command(pass_context=True)
async def afk(ctx):
	""" Declares you afk in chat. Syntax: !afk name """
	msg = '{0.author.mention} is afk'.format(ctx.message)
	await client.say(msg)

# @client.event
# async def on_message_edit(before,after):
# 	await client.send_message(before.channel,"Why did you ("+before.author.mention+") change \""+before.content +"\" to \""+after.content+"\"?")

@client.command(pass_context=True)
async def mock(ctx,*args):
	""" Turns text into SpongeBob mock text. Syntax: !mock text """
	out = ""
	print('{0.author.mention} wrote this'.format(ctx.message))
	for arg in args:
		chars = list(arg.lower())
		for i in range(0, len(chars)):
			if secrets.randbelow(2) == 1:
				out+=chars[i].upper()
			else:
				out+=chars[i]
		out+=" "
	await client.say(out)
	await client.send_file(ctx.message.channel, 'Resourses\Mocking-Spongebob.jpg')


@client.command()
async def community():
	""" Random quote from the TV show 'Community'. Syntax: !community """
	lines = open('community-quotes.txt').read().splitlines()
	line = secrets.choice(lines)
	await client.say(line)

@client.command(pass_context=True)
async def retard(ctx,*args):
	""" Turns text into retard quote. Syntax: !retard quote nameOfPerson"""
	sent = ""
	firstspace = False
	for arg in args[:-1]:
		if firstspace == False:
			firstspace = True
		else:
			sent+=" "
		sent+=arg

	ime = args[-1]
	await client.send_message(client.get_channel(retar),"\""+sent+"\""+" - "+ime)
	await client.delete_message(ctx.message)

@client.command()
async def faggot(*args):
	""" Writes "faggot" within 15 minutes. Syntax : !faggot """
	await asyncio.sleep(secrets.randbelow(900))
	await client.say("faggot")

# @client.event()
# async def on_message(message):
# 	#TODO figure out how to recieve data from twitter.py, fix the import twitter
# 	await client.send_message(message.channel, tekst)
client.loop.create_task(my_background_task())
client.run('NDE4MDIxNDA4NzMyNDc5NDg5.DXbiaw.CgeUtjLAXvzunvjkWIdOKrQubOY')
#  @client.command()
# async def bye(*args):
# 	Application.Start(yourexename.exe);
# 	await discord.Disconnect();


#SLEEP WAIT PAUSE
#await asyncio.sleep(3)
