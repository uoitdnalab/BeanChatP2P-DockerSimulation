#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

BASE_IP_STR = "172.18.1."

NETWORK_ROWS = int(sys.argv[1])
NETWORK_COLS = int(sys.argv[2])

THIS_NODE = int(sys.argv[3])

connections_list = []

for y in range(1, NETWORK_ROWS+1):
	for x in range(1, NETWORK_COLS+1):
		#Each node is connected to it's top, bottom, left, right provided that it exists.
		neighbour_list = []
		
		#left neighbour will have address NETWORK_COLS*(y-1) + x - 1
		left_neighbour = NETWORK_COLS*(y-1) + x - 1
		#check if left_neighbour exists
		if x - 1 > 0:
			#Register the left neighbour of this node
			ip_address = BASE_IP_STR + str(left_neighbour)
			neighbour_list.append(ip_address)
		
		#right neighbour will have address NETWORK_COLS*(y-1) + x + 1
		right_neighbour = NETWORK_COLS*(y-1) + x + 1
		#check if right_neighbour exists
		if x + 1 <= NETWORK_COLS:
			#Register the right neighbour of this node
			ip_address = BASE_IP_STR + str(right_neighbour)
			neighbour_list.append(ip_address)
		
		#top neighbour will have address NETWORK_COLS*(y-2) + x
		top_neighbour = NETWORK_COLS*(y-2) + x
		#check if top_neighbour exists
		if y > 1:
			#Register the top neighbour of this node
			ip_address = BASE_IP_STR + str(top_neighbour)
			neighbour_list.append(ip_address)
		
		#bottom neighbour will have address NETWORK_COLS*y + x
		bottom_neighbour = NETWORK_COLS*y + x
		#check if bottom_neighbour exists
		if y < NETWORK_ROWS:
			#Register the bottom neighbour of this node
			ip_address = BASE_IP_STR + str(bottom_neighbour)
			neighbour_list.append(ip_address)
		
		#Register all connections for this node
		connections_list.append(neighbour_list)

#Display all connections
"""
for i in range(1,NETWORK_COLS*NETWORK_ROWS+1):
	print BASE_IP_STR + str(i)
	print "----------------------------------"
	for neighbour in connections_list[i-1]:
		print neighbour
	print ""
	print ""
	print ""
"""

#Generate all calls to java NetworkAdvertise for each node
"""
for i in range(1,NETWORK_COLS*NETWORK_ROWS+1):
	print BASE_IP_STR + str(i)
	print "----------------------------------"
	for neighbour in connections_list[i-1]:
		print "java NetworkAdvertise Pi_" + str(i)  + " " + str(neighbour)
	print ""
	print ""
	print ""
"""

#Generate all calls to java NetworkAdvertise for this node only
for neighbour in connections_list[THIS_NODE-1]:
		#print "java NetworkAdvertise Pi_" + str(THIS_NODE)  + " " + str(neighbour)
		#print "while true; do java NetworkAdvertise Pi_" + str(THIS_NODE)  + " " + str(neighbour) + "; sleep 5; done &"
		print "while true; do java NetworkAdvertise Pi_" + str(THIS_NODE)  + " " + str(neighbour) + "; sleep $[ ( $RANDOM % 15 ) + 5]; done &"

