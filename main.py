#Imports
import discord
from discord.ext import commands
import loadconfig 
from serverstatus import ServerStatus
import asyncio

#===========================================================================================================================#
#Init stuff
#Setze Prefix für die Commands.
bot = commands.Bot(command_prefix=loadconfig.__prefix__)
mt2server = ServerStatus(loadconfig.__gamepath__,loadconfig.__gamecores___,loadconfig.__dbcore__,loadconfig.__authcore__,loadconfig.__game99core__)
channelcount = loadconfig.__channelcount__

#===========================================================================================================================#
#checks

#Prüfe erlaubte Channel
def check_allowed_channel(ctx):
	return ctx.message.channel.id == int(loadconfig.__botadminchannel__) or ctx.message.channel.id == int(loadconfig.__botuserchannel__)


#===========================================================================================================================#
#Commands#

#Status Command. Gibt den Status vom Server wieder.
@commands.command(aliases=['status', 'Status'])
@commands.cooldown(1,30,commands.cooldowns.BucketType.channel) #30 Sekunden cooldown auf !status
@commands.check(check_allowed_channel)
async def serverstatus(ctx, *args):
	'''Gibt den Onlinestatus des Servers aus'''
	response = ""
	i = 0
	statuses = mt2server.checkServerCommand() #Rufe aktuellen Serverstatus
	chstatus = []	
	auth = loadconfig.__authcore__
	game99 = loadconfig.__game99core__
	db = loadconfig.__dbcore__
	#Daten Sammeln
	for status in statuses:
		for i in range(1, channelcount+1): #gehe alle Channel durch
			if status["Channel"] == "Channel " + str(i):
				chstatus.append(status)
			elif status["Channel"] == auth[1]:
				authstatus = status
			elif status["Channel"] == game99[1]:
				game99status = status
			elif status["Channel"] == db[1]:
				dbstatus = status
	

	#Nachricht Formatieren
	for i in range(1, channelcount+1): #Channel Formatieren
		response+= "Status zu Channel %i : \n" % (i) #Überschrift
		for status in chstatus:			
			if status["Channel"] == "Channel " + str(i):
				response+="%s ist: %s \t" % (status["Core"],status["Status"])
		response+="=================================================\n"
	response+="%s ist: %s \t" % (game99status["Channel"],game99status["Status"])
	response+="%s ist: %s \t" % (authstatus["Channel"],authstatus["Status"])
	response+="%s ist: %s \t" % (dbstatus["Channel"],dbstatus["Status"])
	await ctx.send(response)

@bot.command(hidden=True) #adds command automaticly
async def shdown(ctx):
	'''Fährt den Bot herunter'''
	if await ctx.bot.is_owner(ctx.author):
		await ctx.send('**:ok:** Bye!')
		await bot.logout()
		sys.exit(0)
	else:
		await ctx.send('**:no_entry:** Ich lass mir nur was von Yuudatchi sagen!')

#Bot Commands zuweisen
bot.add_command(serverstatus)
#===========================================================================================================================#
#Bot Trigger

#Wenn bot Erfolgreich gestartet
@bot.event
async def on_ready():
	print('Logged in as')
	print(f'Bot-Name: {bot.user.name}')
	print("Bot gestartet.")
	print('------')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=loadconfig.__servername__))

#Wenn Bot Nachricht erhällt
@bot.event
async def on_message(message):
	if isinstance(message.channel, discord.DMChannel): #ignore PMs
		await message.author.send("Yuudatchi sagt, ich darf nicht mit fremden Leuten reden.")
		return
	await bot.process_commands(message) #Wenn Command, weiter machen.

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CommandOnCooldown): #Wenn on cooldown
		seconds = str(error)[34:]
		await ctx.send(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut')
	if isinstance(error, commands.errors.CheckFailure): # Wenn nicht im Botchannel geschickt
		return


@bot.event
async def checkServerCrash():
	current = ""
	new = ""
	await bot.wait_until_ready() #erst weiter machen wenn Bot Geladen hat
	channel = bot.get_channel(int(loadconfig.__botadminchannel__)) #Admin Channel auswählen
	await channel.send("Server wird nun Überwacht.")
	current = mt2server.checkServer()
	while not bot.is_closed(): #Solange bis Bot beendet wird	
		new = mt2server.checkServer()	
		msg = mt2server.analyseStatus(current, new)
		current = new
		if msg != "":
			await channel.send("===========================================")
			await channel.send("!!Der Status des Servers hat sich geändert!!")
			await channel.send(msg)
		await asyncio.sleep(loadconfig.__checktime__) #Warte X Sekunden bis wiederholung


#===========================================================================================================================#
#Main stuff

#Bot starten
bot.loop.create_task(checkServerCrash())
bot.run(loadconfig.__token__)

