import psutil
import os
import loadconfig
from pathlib import Path

class ServerStatus():
	'''Klasse die den Status des Servers überprüft'''
	__path = ""
	__gamecoreinfo = []
	__servertatus = []
	__dbcoreinfo = []
	#__currentstatus = []
	
	def __init__(self,path,gameserverinfo,dbcoreinfo,authcoreinfo,game99coreinfo):
		self.__path = path
		self.__gamecoreinfo = gameserverinfo
		self.__gamecoreinfo.append(authcoreinfo)
		self.__gamecoreinfo.append(game99coreinfo)
		self.__dbcoreinfo = dbcoreinfo

	def __clearServerStatusList(self):
		'''Setzt den Status für den Server auf offline'''
		self.__servertatus.clear() #leere Server Status
		for serverinfo in self.__gamecoreinfo:
			self.__servertatus.append({"Channel" : serverinfo[1], "Core": serverinfo[2] ,"Status" : ":x:"}) # setze alle auf Offline :x: 
		self.__servertatus.append({"Channel" : self.__dbcoreinfo[1], "Core": ""  ,"Status" : ":x:"}) #setze DB auf offline :x:  

	def checkServerCommand(self):
		'''Prüft ob Server Online sind'''
		self.__clearServerStatusList() #Setze liste zurück
		for proc in psutil.process_iter(): #durch laufe alle Aktiven Prozesse
			try:
				if proc.name() == "game": #Suche nach GAME Prozesse
					for serverinfo in self.__gamecoreinfo: #Ordne game Prozess dem Channel/core zu
						if proc.cwd() == self.__path + serverinfo[0]:
							next((item for item in self.__servertatus if item["Channel"] == serverinfo[1] and item["Core"] == serverinfo[2]),False)["Status"] = ":white_check_mark:"#Setze Server Status auf Online
				if proc.name() == "db": #Suche nach db core Prozess	
					next((item for item in self.__servertatus if item["Channel"] == self.__dbcoreinfo[1]),False)["Status"] = ":white_check_mark:" #:white_check_mark: 
			except (psutil.AccessDenied, psutil.ZombieProcess):
				pass #Wenn Zugriff auf Process Verweigert wird oder Prozess ein Zombie Prozess ist
		return self.__servertatus


	def __doesProcessExist(self,cwd):
		'''Finde Prozess nach dem working dict'''
		for proc in psutil.process_iter():
			try:
				return proc.cwd() == cwd #true wenn gefunde fals wenn nicht
			except (psutil.AccessDenied, psutil.ZombieProcess):
				pass


	def checkServer(self):
		currentstatus = []
		for gamecore in self.__gamecoreinfo:
			try:
				file = self.__path + gamecore[0] + "/pid"
				f = open(file,'r')								#Suche nach allen pid files
				if psutil.pid_exists(int(f.read())):			#Prüfe ob Process aus pid existiert
					currentstatus.append({"name" : gamecore[0], "pid" : True, "running" : True})
				else:
					currentstatus.append({"name" : gamecore[0], "pid" : True, "running" : False})
			except FileNotFoundError:							#Wenn pid nicht existiert
				if self.__doesProcessExist(self.__path + gamecore[0]):  #Prüfe ob Process vorhanden
					currentstatus.append({"name" : gamecore[0], "pid" : False, "running" : True})
				else:
					currentstatus.append({"name" : gamecore[0], "pid" : False, "running" : False})
		return currentstatus

	def analyseStatus(self,oldstatus,newstatus):
		message = ""
		if oldstatus == newstatus:
			return message 
		else: #wenn sich was geändert hat
			for old , new in zip(oldstatus,newstatus):
				if old == new:
					continue #Dieser Status hat sich nicht geändert. Nächster
				else:
					if new["pid"] == True and new["running"] == True: #Server läuft
						message+="INFO: %s ist wieder online! \n" % (new["name"])
					elif new["pid"] == True and new["running"] == False: #PID aber kein Prozess ist meistens ein Crash
						message+="WARN:  %s ist eventuell gecrasht! PID gefunden aber kein Prozess!\n" % (new["name"])
						coredump= Path(self.__path + new["name"] + "/game.core")
						if coredump.exists():
							message+="Coredump detected."
					elif new["pid"] == False and new["running"] == True: #Wenn jemand nicht aufpasst oder so. idk
						message+="WARN: %s wurde keine PID gefunden, Prozess läuft aber. Eventuell gelöscht? \n" % (new["name"])
					elif new["pid"] == False and new["running"] == False: #Wenn Server normal Heruntergefahren wird
						message+="INFO: %s ist Offline. Normaler Shutdown. \n" % (new["name"])
		return message
