#!/usr/bin/env python2.7
# encoding: utf-8
"""
MacJournalToDayOne.py

Created by kdm on 2010-02-10.
Updated on 2019-08-03 to work with Day One 2.0

Copyright (c) 2010 __MyCompanyName__. All rights reserved.
Copyright (c) 2019 Sasmito Adibowo. All rights reserved.

"""

import sys
import time
from datetime import date
from datetime import timedelta
from time import strptime
import os
import string
import subprocess
import shlex
import optparse
import logging
from shutil import copyfileobj

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
#Parse input variables
	
	main_logger = logging.getLogger('main')

	usage = "usage:  %prog [options] <MacJournal Export File to import>"
	parser = optparse.OptionParser(usage=usage)
	
	parser.add_option("--debug", dest="debug", default=True, action = "store_true", help = "Turn on debug output (default true)")
	parser.add_option("--journal", dest='target_journal', default="MacJournal Import", action = "store", help = "Specify the target journal name in Day One (default is 'MacJournal Import')")
	
	(options, args) = parser.parse_args()
	
	if len(args) != 1:
		parser.error("File to import required")
	else:
		journal_name = args[0]	
	
	if options.debug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.ERROR)
	
	print "Target journal: {0}".format(options.target_journal)

	try:
		journal = open(journal_name,'r')
	except:
		main_logger.error("Could not open %s" % journal_name)
		return 1 # Could not open journal

	numEntries = 0
	prevEntryDate = None
	journalEntry = None
	curEntryLines = 0
	prevEntryLines = 0
	continueLoop = True
	entryDone = False
	curEntryDate = None
	prevEntry = ''
	curEntry = ''
	prevEntryTopic = ''
	curEntryTopic = ''

	#Due to python's lack of a DO/UNTIL statement, have to do things a bit differently
	
	while continueLoop is True:
	
		entryLine = journal.readline()
	
		if not entryLine: #Reached EOF
			entryDone = True
			continueLoop = False
			prevEntryDate = curEntryDate
			prevEntry = curEntry
			prevEntryLines = curEntryLines
			curEntry = ''
			curEntryLines = 0

			main_logger.debug("Reached EOF")
	
		if entryLine.startswith("\tDate:\t"): # An entry is finished
			prevEntryDate = curEntryDate
			prevEntry = curEntry
			prevEntryLines = curEntryLines
			curEntry = ''
			curEntryLines = 0
			curEntryDate = entryLine.replace("\tDate:\t",'').rstrip()
			entryDone = True
			main_logger.debug("Found entry: {0}".format(curEntryDate))
		elif entryLine.startswith('\tTopic:\t'): # The current entry topic
			prevEntryTopic = curEntryTopic
			curEntryTopic = entryLine.replace('\tTopic:\t','').rstrip()
		elif entryLine is not "":
			curEntry += entryLine
			curEntryLines += 1

		if (entryDone is True) and (prevEntryLines is not 0):
			#Write output to DayOne
			main_logger.info('{0} has {1} lines with topic "{2}"'.format(prevEntryDate,repr(prevEntryLines), prevEntryTopic))
			addCommandParsed = ['dayone2', 'new', 
				'-d', '{0}'.format(prevEntryDate),
				'-j', '{0}'.format(options.target_journal)
				]
			try:
				main_logger.debug("dayone2 {0}".format(addCommandParsed))
				addCommandProcess = subprocess.Popen(addCommandParsed,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			except:
				None
			formatEntry = "{0}\n{1}\n".format(prevEntryTopic, prevEntry)
			addCommandOut = addCommandProcess.communicate(formatEntry)
			main_logger.info("STDOUT from dayone2: {0}".format(addCommandOut[0]))
			main_logger.info("STDERR from dayone2: {0}".format(addCommandOut[1]))
			addCommandProcess.wait()
			returnCode = addCommandProcess.returncode
			if returnCode != 0:
				main_logger.error("DayOne failed to import entry dated {0} with error code {1}".format(prevEntryDate, returnCode))
				break
			numEntries += 1
			entryDone = False
			prevEntryDate = None
			prevEntry = None
			prevEntryLines = 0


	main_logger.info("Found %s entries" % numEntries)
	
	journal.close()
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
