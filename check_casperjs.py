#!/usr/bin/env python
# Copyright (c) 2018 Matt Capra (http://www.mcapra.com)
#
# This software is provided under the Apache Software License. 
#
# Description: This Nagios plugin runs and parses a CasperJS test case.
# 
# Author:
#  Matt Capra

import argparse
import commands
import logging
import time
import re

def check_casperjs():
	nagios_exit = {}
	if(args.binary):
		output = commands.getoutput(args.binary + ' test ' + args.path)
	else:
		output = commands.getoutput('casperjs test ' + args.path)
		
	# Used to strip ANSI codes that CasperJS uses to make the output "pretty"
	ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
	output = ansi_escape.sub('', output)
	
	if(args.verbose):
		print str(output)
		
	lines = output.splitlines()
	output_parse = re.compile('(([A-Z]{4}).*in\\s(\\d+\\.\\d+)s,\\s([0-9]*)\\spassed,\\s([0-9]*)\\sfailed,\\s([0-9]*)\\sdubious.*)')
	parsed = []
	failures = ''
	passes = ''
	# todo - gracefully handle CasperJS runtime errors
	for line in lines:
		if(re.match('FAIL\\s(?!.*executed in)', line)):
			failures += '(' + line + ') '
		elif(re.match('PASS\\s(?!.*executed in)', line)):
			passes += '(' + line + ') '
		else:
			m = re.match(output_parse, line)
			if(m):
				parsed = re.findall(output_parse, line)
				break
	
	# todo - gracefully handle | character in status output
	# todo - remove some trailing spaces
	if(parsed[0][1] == 'PASS'):
		#if we pass
		nagios_exit['status'] = 'OK - ' + parsed[0][0]
		if(args.report):
			nagios_exit['status'] += passes
		nagios_exit['code'] = 0
		nagios_exit['perfdata'] = '|runtime=' + parsed[0][2] + 's'
	elif(parsed[0][1] == 'FAIL'):
		#if we fail, there should be a summary to print
		nagios_exit['status'] = 'CRITICAL - ' + parsed[0][0]
		if(args.report):
			nagios_exit['status'] += failures
		nagios_exit['code'] = 2
		nagios_exit['perfdata'] = '|runtime=' + parsed[0][2] + 's'
	else:
		nagios_exit['status'] = 'UNKNOWN - ' + output
		nagios_exit['code'] = 3

	return nagios_exit

if __name__ == '__main__':
	import cmd
	
	parser = argparse.ArgumentParser(add_help = True, description = "Executes CasperJS test cases and reports any errors found.")

	parser.add_argument('-p', '--path', action='store', help='The logical path to the CasperJS script you want to check.', required=True)
	parser.add_argument('-w', '--warning', action='store', help='The warning threshold for the script\'s execution time (in seconds).', required=False)
	parser.add_argument('-c', '--critical', action='store', help='The critical threshold for the script\'s execution time (in seconds).', required=False)
	parser.add_argument('-a', '--args', action='store', help='Any arguments you want to pass to your CasperJS script.', required=False)
	parser.add_argument('-r', '--report', action='store_true', help='Include a report of each test step in the status output (can be useful for diagnosing failures).', required=False)
	parser.add_argument('-b', '--binary', action='store', help='Path to the CasperJS binary you wish to use.', required=False)
	parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (this can be VERY long).', required=False)
	
	args = parser.parse_args()

	nagios_exit = {}
	
	nagios_exit = check_casperjs()
	
	print(nagios_exit['status'] + nagios_exit['perfdata'])
	exit(nagios_exit['code'])
