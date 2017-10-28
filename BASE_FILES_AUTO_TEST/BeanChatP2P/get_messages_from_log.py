#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#log_file = open(sys.argv[1],'r')

#log_line = log_file.readline()
log_line = sys.stdin.readline()

output_index = 0
message_state = False
output_file = ""

while log_line:
	
	if message_state and log_line.find("------ END OF OUR MESSAGE ------") == -1:
		output_file.write(log_line)
	
	if log_line.find("------ WE HAVE A MESSAGE FOR US ------") != -1 and not message_state:
		output_file = open("rx_messages/message_file_" + str(output_index).zfill(4),'w')
		message_state = True
	
	if log_line.find("------ END OF OUR MESSAGE ------") != -1:
		message_state = False
		output_file.close()
		output_index = output_index + 1
	
	#log_line = log_file.readline()
	log_line = sys.stdin.readline()

#log_file.close()
