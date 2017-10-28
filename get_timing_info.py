#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import sys


CHECK_NODES = 4 # (2x2) = 4
#CHECK_NODES = 9 # (3x3) = 9
#CHECK_NODES = 16 # (4x4) = 16
#CHECK_NODES = 25 # (5x5) = 25
#CHECK_NODES = 36 # (6x6) = 36

start_time = time.time()

#Search all directories for expected files
mounted_dirs = os.listdir('__mounts')

transfer_complete = False

while not transfer_complete:
	is_done = True 
	for d in mounted_dirs:
		messages = os.listdir('__mounts/' + d)
		#Scan through all messages
		senders_list = []
		for m in messages:
			message_file = open('__mounts/' + d + '/' + m)
			message_content = message_file.read()
			message_file.close()
			message_sender = message_content.split(' ')[0]
			senders_list.append(message_sender)
		
		
		#Check senders_list
		this_node = int(d[10:])
		this_node_id = 'Pi_' + str(this_node)
		
		test_nodes = []
		for i in range(1, CHECK_NODES + 1):
			if i != this_node:
				test_nodes.append('Pi_' + str(i))
		
		print str(this_node_id) + " : " + str(senders_list)
		
		for n in test_nodes:
			if n not in senders_list:
				is_done = False
		
		transfer_complete = is_done


elapsed_time = time.time() - start_time

print "Total test time: " + str(elapsed_time)
