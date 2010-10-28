################################################################################
#
# This program is part of the FormulaDataSource Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenUtils.Utils import getExitMessage
from Products.ZenRRD.CommandParser import CommandParser

class formula(CommandParser):

	#this method is the only one required for a zencommand parser
	#its purpose is to store the results into the RRD files
	def processResults(self, cmd, result):
		#grab the output resulting from the command
		output = cmd.result.output
		output = output.split('\n')[0].strip()
		#get the exit code from the command
		# not exactly sure what it means
		exitCode = cmd.result.exitCode
		#gets the severityt that is associated with the command
		severity = cmd.severity
		#output looks like eg ("guestperf|memUsage=1000 ...")
		#make sure we are getting the correct output
		if output.find('|') >= 0:
			#msg = substring left of the |
			#values = substring right of the |
			msg, values = output.split('|', 1)
		else:
			#msg = output
			#values = ''
			msg, values = output, ''
		msg = msg.strip() or 'Cmd: %s - Code: %s - Msg: %s' % (cmd.command, exitCode, getExitMessage(exitCode))
		if exitCode != 0:
			result.events.append(dict(device=cmd.deviceConfig.device,
									  summary=msg,
									  severity=severity,
									  message=msg,
									  performanceData=values,
									  eventKey=cmd.eventKey,
									  eventClass=cmd.eventClass,
									  component=cmd.component))

		for value in values.split(' '):
			if value.find('=') > 0:
				label, val = value.split('=')
				for dp in cmd.points:
					if dp.id == label:
						result.values.append( (dp, val) )
						break
