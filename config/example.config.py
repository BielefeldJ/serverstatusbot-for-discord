#Discord Stuff
#Discord Bot token
__token__ = 'YOUR TOKEN HERE' 
#Command Prefix	
__prefix__ = '!' 								
#Servername wird in Discord angezeigt als BotUsername is whatching <servername> 
__servername__ = '' 	
#Channel wo Crashinfos rein kommen
__botadminchannel__ = 'CHANNEL ID'
#Channel für user !status command
__botuserchannel__ = 'CHANNEL ID' 
#Intervall in dem der Server gepüft werden woll in Sekunden
__checktime__ = 10


#Gameserver stuff 
#Anzahl Channel
__channelcount__ = 4
#Path zum Gameserver root
__gamepath__ = '/usr/home/game' 							
#Liste an Channel / Cores  
__gamecores___ = [
	#("Path vom __gamepath__", "Channel Bezeichnung", "Core Bezeichnung",)
	#channel 1
	("/channel1/core1","Channel 1","Core 1"),
	("/channel1/core2","Channel 1","Core 2"),
	("/channel1/core3","Channel 1","Core 3"),
	("/channel1/empires","Channel 1","Empires"),
	#channel 2
	("/channel2/core1","Channel 2","Core 1"),
	("/channel2/core2","Channel 2","Core 2"),
	("/channel2/core3","Channel 2","Core 3"),
	("/channel2/empires","Channel 2","Empires"),
	#channel 3
	("/channel3/core1","Channel 3","Core 1"),
	("/channel3/core2","Channel 3","Core 2"),
	("/channel3/core3","Channel 3","Core 3"),
	("/channel3/empires","Channel 3","Empires"),
	#channel 4
	("/channel4/core1","Channel 4","Core 1"),
	("/channel4/core2","Channel 4","Core 2"),
	("/channel4/core3","Channel 4","Core 3"),
	("/channel4/empires","Channel 4","Empires")		
]
#channel 99     #("Path vom __gamepath__", "Channel Bezeichnung", "",)
__game99core__ = ("/game99","Channel 99", "")
#login Server #("Path vom __gamepath__", "Channel Bezeichnung", "",)
__authcore__ = ("/auth","Login Server" , "" )
#db Server   (path,name)
__dbcore__ = ("/db","Datenbankanbindung") 