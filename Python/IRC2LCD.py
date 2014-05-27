#! /usr/bin/env python
#
# IRC2LCD
# Tim Ballas
#
"""IRC bot to display mentions on an LCD through a Parallax Propeller.

Usage: IRCbot2LCD.py <server[:port]> <channel> <nicknameToMonitor> <COMport> <optional bot nickname>

"""
#
# Modified from:
# Example program using irc.bot.
# Joel Rosdahl <joel@rosdahl.net>
#

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import re
import serial
import time


class IRC2LCDbot(irc.bot.SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel

	def on_nicknameinuse(self, c, e):
		c.nick(BotNick)

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_pubmsg(self, c, e):
		pubmsgTemp = e.arguments[0]														# e.arguments[0] is the public message we are processing, loaded into "pubmsgTemp"
		pattern = re.compile(r'(.*{0}\s.*|.*{1}:.*)'.format(MonitorNick,MonitorNick))	# Compile Regular Expression to check if the public message has our MonitorNick in it
		result = re.search(pattern, pubmsgTemp)											# Execute Regular Expression
		if result:																		# Check to see if we matched our MonitorNick in the public message
			try:																		# Handle error when result has 'None' in it
				print result.group(1)													# Print matched message to the console
				MatchedMessage = str(result.group(1))									# Load matched message into "MatchedMessage" variable. Enclosing it in "str()" is to return a nice printable string.
				ser.write("\r\t" + MatchedMessage)										# Write "MatchedMessage" to LCD through Parallax Propeller over Serial connection. "\r\t" is command for Propeller to Clear LCD.
			except:																		# Needed to complete 'try:' statement
				pass																	# Do nothing and move on

def main():
	import sys
	if len(sys.argv) < 5:
		print("Usage: IRCbot2LCD.py <server[:port]> <channel> <nicknameToMonitor> <COMport> <optional bot nickname>")
		sys.exit(1)

	s = sys.argv[1].split(":", 1)
	server = s[0]
	if len(s) == 2:
		try:
			port = int(s[1])
		except ValueError:
			print("Error: Erroneous port.")
			sys.exit(1)
	else:
		port = 6667
	channel = sys.argv[2]
	nickname = sys.argv[3]
	COMport = sys.argv[4]
	
	global BotNick												# Declare global variable for "BotNick"
	if len(sys.argv) == 6:										# If there is a argument defined for "BotNick"
		BotNick = sys.argv[5]									# Set "BotNick" to Argument 5(sys.argv[5])
	else:														# Else
		BotNick = nickname + "_"								# Use nickname to monitor and an underscore
	
	global MonitorNick											# Declare global variable for "MonitorNick"
	MonitorNick = nickname										# Set "MonitorNick" to nickname(sys.argv[3])
	
	global ser													# Declare global variable for "ser"
	ser = serial.Serial(str(COMport),baudrate=9600)				# Set "ser" to Serial object
	
	bot = IRC2LCDbot(channel, nickname, server, port)			# Set "bot" to IRC2LCDbot object
	bot.start()													# Start bot
	ser.close()													# Closing Serial port will prevent problems

if __name__ == "__main__":
	main()
