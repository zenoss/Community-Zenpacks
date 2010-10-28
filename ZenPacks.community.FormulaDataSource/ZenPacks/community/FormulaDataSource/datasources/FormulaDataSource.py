################################################################################
#
# This program is part of the FormulaDataSource Zenpack for Zenoss.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions

from Products.ZenEvents.ZenEventClasses import Cmd_Fail
from Products.ZenUtils.Utils import executeStreamCommand
from Products.ZenWidgets import messaging

import cgi, time, string

# Command template
cmdTemplate = ("${here/ZenPackManager/packs/ZenPacks.community.FormulaDataSource/path}/libexec/calc_formula.py --device='${dev/manageIp}' --datasource='%s' --formula='%s'")

class FormulaDataSource(RRDDataSource.SimpleRRDDataSource, ZenPackPersistence):

	ZENPACKID = 'ZenPacks.community.FormulaDataSource'

	sourcetypes = ('FORMULA',)
	sourcetype = 'FORMULA'
	parser = 'ZenPacks.community.FormulaDataSource.parsers.formula'
	dataformula = ''
	
	# Properties which are used in edit datasource
	_properties = RRDDataSource.RRDDataSource._properties + (
		{'id':'dataformula', 'type':'string', 'mode':'w'},
		)

	_relations = RRDDataSource.RRDDataSource._relations + (
		)

	# Screen action bindings (and tab definitions)
	factory_type_information = (
	{
		'immediate_view' : 'editFormulaDataSource',
		'actions' 		 :
		(
			{ 'id'			: 'edit'
			, 'name'		: 'Data Source'
			, 'action'		: 'editFormulaDataSource'
			, 'permissions'	: ( Permissions.view, )
			},
		)
	},
	)

	security = ClassSecurityInfo()

	def getDescription(self):
		return self.dataformula

	# This tells zenoss that the datasource uses zencommand to collect the data
	def useZenCommand(self):
		return True

	# This method gets the command that will be run with zencommand	
	def getCommand(self, context):
		# Replace shell variable characters before passing to script.
		formula = self.dataformula.replace("$", "%")
		# Define the command.
		cmd = cmdTemplate % (self.soleDataPoint().id,formula)
		cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
		return cmd

	# This method is used to test the datasource in the edit datasource window
	def testDataSourceAgainstDevice(self, testDevice, REQUEST, write, errorLog):

		out = REQUEST.RESPONSE
		# Determine which device to execute against
		device = None
		if testDevice:
			# Try to get specified device
			device = self.findDevice(testDevice)
			if not device:
				errorLog(
					'No device found',
					'Cannot find device matching %s' % testDevice,
					priority=messaging.WARNING
				)
				return self.callZenScreen(REQUEST)
		elif hasattr(self, 'device'):
			# ds defined on a device, use that device
			device = self.device()
		elif hasattr(self, 'getSubDevicesGen'):
			# ds defined on a device class, use any device from the class
			try:
				device = self.getSubDevicesGen().next()
			except StopIteration:
				# No devices in this class, bail out
				pass
		if not device:
			errorLog(
				'No Testable Device',
				'Cannot determine a device to test against.',
				priority=messaging.WARNING
			)
			return self.callZenScreen(REQUEST)

                header = ''
                footer = ''
                # Render
                if REQUEST.get('renderTemplate', True):
                    header, footer = self.commandTestOutput().split('OUTPUT_TOKEN')

                out.write(str(header))

		# Get the command to run
		command = None
		if self.sourcetype=='FORMULA':
			command = self.getCommand(device)
		else:
			errorLog(
                'Test Failure',
                'Unable to test %s datasources' % self.sourcetype,
                priority=messaging.WARNING
            )
			return self.callZenScreen(REQUEST)
		if not command:
			errorLog(
                'Test Failure',
                'Unable to create test command.',
                priority=messaging.WARNING
            )
			return self.callZenScreen(REQUEST)
		# Render
		header = ''
		footer = ''
		out.write(str(header))

		write("Calculating formula '%s' against %s" %(self.dataformula, device.id))
		write('')
		start = time.time()
		try:
			executeStreamCommand(command, write)
		except:
			import sys
			write('Exception while calculating formula')
			write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
		write('')
		write('')
		write('DONE in %s seconds' % long(time.time() - start))
		out.write(str(footer))

	security.declareProtected('Change Device', 'manage_testDataSource')
	def manage_testDataSource(self, testDevice, REQUEST):
		''' Test the datasource by executing the command and outputting the
		non-quiet results.
		'''
		# set up the output method for our test
		out = REQUEST.RESPONSE
		def write(lines):
			''' Output (maybe partial) result text.
			'''
			# Looks like firefox renders progressive output more smoothly
			# if each line is stuck into a table row.
			startLine = '<tr><td class="tablevalues">'
			endLine = '</td></tr>\n'
			if out:
				if not isinstance(lines, list):
					lines = [lines]
				for l in lines:
					if not isinstance(l, str):
						l = str(l)
					l = l.strip()
					l = cgi.escape(l)
					l = l.replace('\n', endLine + startLine)
					out.write(startLine + l + endLine)

		errorLog = messaging.IMessageSender(self).sendToBrowser
		return self.testDataSourceAgainstDevice(testDevice, REQUEST, write, errorLog)
