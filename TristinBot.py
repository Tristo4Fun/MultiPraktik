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
import io
from bs4 import BeautifulSoup
#reading channel info
ch = open('channels.txt').read().splitlines()
risk = ch[0]
retar = ch[1]
daily = ch[2]

dict = {'ExampleKey1 ':'ExapleDefinition1',
'ExampleKey2 ':'ExapleDefinition2',
'ExampleKey3 ':'ExapleDefinition3'}

dictLines = open('dictBoy.txt').read().splitlines()
keyLine = ""
valueLine = ""
for line in dictLines:
	if(len(line.split('|'))>1):
		keyLine = line.split('|')[0]
		valueLine = line.split('|')[1]
	dict[keyLine] = valueLine

#initialising Reddit user
reddit = praw.Reddit(client_id='CLIENT ID',client_secret='CLIENT SECRET',user_agent='USER AGENT')

#initialising Imgur user
imgclient_id = 'CLIENT ID'
imgclient_secret = 'CLIENT SECRET'
imgclient = ImgurClient(imgclient_id, imgclient_secret)

client = Bot(description="Najbolji bot north of the wall", command_prefix="!", pm_help = False, )

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
	global votes_up
	global votes_down
	global msgToDelete
	global msgToAddToDict
	global msgToCompare
	global voteOnce
	voteOnce = []
	votes_up = 0
	votes_down = 0
	print("Bot is ready!")
	return await client.change_presence(game=discord.Game(name='Still being developed'))

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
	await client.say("WOOOOOOOOOOOOOOOOOOOOOOOOO LET'S GOOOOOOOOOOOOOO")

@client.command(pass_context = True)
async def killhype(ctx,*args):
	""" Kills hype. Syntax: !killhype """
	await client.delete_message(ctx.message)
	await client.say("*closes game*")

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

#hangman
#currently shows the random word while guessing and doesn't have an ending condition
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
	""" Random drop location in PUBG. Syntax: !drop erangel/miramar """
	erangel = ['Stalber','Woodcutters Camp','Gatka','Mansion','Zharki','School','Farm','Quarry','Prison','Pier Town','Hospital','Swamp town','Kameshki','Shelter','Yasnaya Polyana','Novorepnoye','Georgopol','Severny','Pochinki','Lipovka','Mylta Power','Primorsk','Shooting Range','Rozhok','Mylta','Military Base','Water Town','Ruins','Split (everyone has their own houses)','Crate Hunt (choose small drop near cars)']
	miramar=['Power Grind','San Martin','El Pozo','Ladrillera','Minas Generales','Torre Ahumada','Campo Militiar','Trailer Park','El Azahar','Impala','Ruins','Hacienda del Patron','Tierra Bronca','La Cobreria','Minas del Sur','La Bendita','Valle del Mar','Crater Fields','Puerto Paraiso','Minas del Valle','Water Treatment','Los Higos','Prison','Chumacera','Junkyard','Los Leones','Monte Nuevo','Pecado','Cruz del Valle','Graveyard''Split (everyone has their own houses)','Crate Hunt (choose small drop near cars)']
	i=secrets.randbelow(len(erangel)-1)
	k=secrets.randbelow(len(miramar)-1)
	if ctx.upper()=='MIRAMAR':
		await client.say('Drop at ' + miramar[k])
	elif ctx.upper()=='ERANGEL':
		await client.say('Drop at ' + erangel[i])
	else:
		await client.say('... erangel ili miramar')

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

@client.command(pass_context=True)
async def mock(ctx,*args):
	""" Turns text into SpongeBob mock text. Syntax: !mock text """
	out = ""
	print(args)
	print('{0.author.mention} wrote this'.format(ctx.message))
	for arg in args:
		chars = list(arg)
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
async def quotethis(ctx,*args):
	""" Turns text into a quote. Syntax: !quotethis quote nameOfPerson"""
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
async def bleep(*args):
	""" Writes "bloop" within 15 minutes. Syntax : !bleep """
	await asyncio.sleep(secrets.randbelow(900))
	await client.say("bloop")


@client.command()
async def ebay(*args):
	"""Gets ebay listings. Syntax:!red cup 1 5 | Will get cheapest cup between 1$ and 5$"""
	userSearch = args
	url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="
	#userSearch = userSearch.split(' ')
	for search in userSearch[:-1]:
	    url += search+"+"
	url = url[:-1]
	r_html = requests.get(url).text
	soup = BeautifulSoup(r_html,"html.parser")
	chr = soup.find_all('h3',class_="s-item__title")
	cijene = soup.find_all('span',class_="s-item__price")
	links = soup.find_all('a',class_="s-item__link")
	cijeneFinal = []
	for i in range(0,len(cijene)):
	    #if the parent is the same it means there are 2 or more prices in the same item category and we don't want them to clog up the cijene[] and cause
	    #some items to have wrong prices attached to them so we check for that and remove any prices but the base one
	    if((cijene[i].parent.parent.parent.parent.parent == cijene[i-1].parent.parent.parent.parent.parent)):
	        continue
	    else:
	        cijeneFinal.append(cijene[i])
	values = [len(chr),len(cijeneFinal),len(links)]
	#print(values)
	filterCijena = int(str(userSearch[-1]))
	filterCijenaMin = int(str(userSearch[-2]))
	#print(">"+str(filterCijena))
	class item:
	    ime = None
	    cijena = None
	    cijenaString = None
	    link = None
	    parentTag = None

	replaced = ""
	items = []
	itemsFinal=[]
	#return this after you fix the bid 2 prices on 1 item being treated as 2 prices on 2 items
	for graf in range(min(values)):
	    items.append(item())
	for i in range(0,min(values)):
	    #assigns title text to the ime variable of object
	    if(chr[i].text[0:11].lower() == "new listing"):
	        items[i].ime=chr[i].text[11:]
	    else:
	        items[i].ime = chr[i].text
	    items[i].cijenaString = cijeneFinal[i].text
	    #turning the string we got from the price in the $3.45 format into a 3.45 float
	    if(any(char.isdigit() for char in str(cijeneFinal[i].string))):
	        #if the price has a ',' replace all '.' with '' and all ',' with '.' and remove last 2 digits (the decimal remainder)
	        if(',' in str(cijeneFinal[i].string)[1:]):
	            replaced = str(cijeneFinal[i].string)[1:].replace(".","")
	            replaced = replaced[:-2]
	            replaced = replaced.replace(",",".")
	            items[i].cijena = float(replaced)
	        #if the price doesn't have a ',' juts remove the '$' sign and store it as a float inside the item class
	        else:
	            items[i].cijena = float(str(cijeneFinal[i].string)[1:])
	    #if the price isn't a price at all we set the value to the first decimal of the first number ($0.13 to $13.5) => 0.1
	    else:
	        items[i].cijena = float(str(cijeneFinal[i].text)[1:4])
	        #print("|||"+str(float(str(cijeneFinal[i].text)[1:4])))
	    #we assign the href memeber of the tag to the link variable of object
	    items[i].link = links[i]['href']
	    items[i].parentTag = chr[i].parent.parent.parent

	#sorting the array of objects by attribute cijena
	items.sort(key=lambda x: x.cijena, reverse=False)

	#makes a new list of items and stores the ones that have free shipping in it
	freeShipping = []
	for i in range(0,len(items)):
	    ship = items[i].parentTag.find_all("span",class_="s-item__shipping s-item__logisticsCost")
	    for s in ship:
	        if(s.text=="Free Shipping"):
	            items[i].ime= "***FREE SHIPPING : *** " +items[i].ime
	            freeShipping.append(items[i])

	#merges freeShipping with items
	for x in items:
	    if(x in freeShipping):
	        continue
	    else:
	        freeShipping.append(x)
	br=0
	discordBr = 0
	#prints list of items until upper limit
	for x in freeShipping:
		if(x.cijena != None and x.cijena<filterCijena and x.cijena> filterCijenaMin and x.cijena != -0.5 and discordBr<1):
			await client.say(str(x.ime)+" | "+str(x.cijenaString)+" | "+str(x.link)+"\n")
			discordBr+=1




@client.command()
async def what(*args):
	"""Lookup a meaning of word Syntax : !what _word_ """
	str1 = ' '.join(args)
	str1 = str1+' '
	if(str1 in dict):
		await client.say(str(dict[str1]))


@client.command()
async def dictionary(*args):
	"""Lists all entries in the dictionary"""
	#await client.say(dict.values()[0])
	for a in dict.keys():
		if(a == ""):
			continue
		await client.say(a + " -> " + dict[a])
anotherEntry = 0
@client.command()
async def dictionary_add(*args):
	"""Syntax: !dictionary_add word blahblah definition blah blah"""
	global msgToAddToDict
	global msgToDelete
	global msgToCompare
	key=""
	value=""
	try:
		start_key =args.index("word")
		start_value=args.index("definition")
	except ValueError:
		await client.say("No _word_ or _definition_ in syntax")
		start_value=0
		start_key=0
	for i in range(start_key+1,start_value):
		key+=args[i]
		key+=' '
	for i in range(start_value+1,len(args)):
		value+=args[i]
		value+=' '
	with open('tempDictBoy.txt','w') as file:
		file.write(key+"|"+value)
	msgToCompare = f"Vote with 👍 / 👎 to add/not add this to the dictionary: {key}|{value}"
	msgToAddToDict = key+" | "+value
	msgToDelete = await client.say(msgToCompare)


@client.event
async def on_reaction_add(reaction, user):
	global votes_up
	global votes_down
	global msgToDelete
	global msgToAddToDict
	global msgToCompare
	global voteOnce
	dictionaryString = ""
	dictionaryList = []
	if((reaction.emoji == '👍' and reaction.message.content+" " == msgToCompare) and user.id not in voteOnce):
		voteOnce.append(user.id)
		votes_up+=1
	elif((reaction.emoji == '👎' and reaction.message.content+" " == msgToCompare) and user.id not in voteOnce):
		voteOnce.append(user.id)
		votes_down+=1

	if(votes_up > 2):
		await client.send_message(msgToDelete.channel,f"The entry \"{msgToAddToDict}\" has been added to the dictionary")
		await client.delete_message(msgToDelete)
		with open('tempDictBoy.txt','r') as file:
			dictionaryString = file.read()
		#dictionaryList = dictionaryString.split('|')
		with open('dictBoy.txt','a') as file:
			file.write(dictionaryString + "\n")
		votes_up = 0
		votes_down = 0
		voteOnce = []
	elif(votes_down > 2):
		await client.send_message(msgToDelete.channel,f"The entry \"{msgToAddToDict}\" was not added to the dictionary")
		await client.delete_message(msgToDelete)
		votes_up = 0
		votes_down = 0
		voteOnce = []
	dictLines = open('dictBoy.txt').read().splitlines()
	keyLine = ""
	valueLine = ""
	for line in dictLines:
		if(len(line.split('|'))>1):
			keyLine = line.split('|')[0]
			valueLine = line.split('|')[1]
		dict[keyLine] = valueLine



@client.command(pass_context=True)
async def reply(ctx,*args):
	"""Syntax : !reply message_ID Your response"""
	msg = await client.get_message(ctx.message.channel, args[0])
	await client.say(f" ```{msg.author.name} : {msg.content}``` "+ctx.message.author.name+" : "+' '.join(args[1:]))
	await client.delete_message(ctx.message)




client.loop.create_task(my_background_task())
client.run('BOT TOKEN')
