try:
    from config.config import __token__, __prefix__, __servername__, __botadminchannel__,__botuserchannel__,__gamepath__,__gamecores___,__dbcore__,__channelcount__,__game99core__,__authcore__,__checktime__
except ImportError:
	print("Fehler beim Laden der Config!")
	exit()