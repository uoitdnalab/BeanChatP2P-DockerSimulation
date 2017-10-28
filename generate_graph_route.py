#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx

BASE_IP_STR = "172.18.1."

NETWORK_ROWS = int(sys.argv[1])
NETWORK_COLS = int(sys.argv[2])

THIS_NODE = int(sys.argv[3])
DEST_NODE = int(sys.argv[4])

connections_list = []

network_graph = nx.Graph()

for y in range(1, NETWORK_ROWS+1):
	for x in range(1, NETWORK_COLS+1):
		
		#Create this node on the nx graph
		this_node = NETWORK_COLS*(y-1) + x
		network_graph.add_node("Pi_" + str(this_node))
		
		#Each node is connected to it's top, bottom, left, right provided that it exists.
		neighbour_list = []
		
		#left neighbour will have address NETWORK_COLS*(y-1) + x - 1
		left_neighbour = NETWORK_COLS*(y-1) + x - 1
		#check if left_neighbour exists
		if x - 1 > 0:
			#Register the left neighbour of this node
			ip_address = BASE_IP_STR + str(left_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge("Pi_" + str(this_node), "Pi_" + str(left_neighbour))
		
		#right neighbour will have address NETWORK_COLS*(y-1) + x + 1
		right_neighbour = NETWORK_COLS*(y-1) + x + 1
		#check if right_neighbour exists
		if x + 1 <= NETWORK_COLS:
			#Register the right neighbour of this node
			ip_address = BASE_IP_STR + str(right_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge("Pi_" + str(this_node), "Pi_" + str(right_neighbour))
		
		#top neighbour will have address NETWORK_COLS*(y-2) + x
		top_neighbour = NETWORK_COLS*(y-2) + x
		#check if top_neighbour exists
		if y > 1:
			#Register the top neighbour of this node
			ip_address = BASE_IP_STR + str(top_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge("Pi_" + str(this_node), "Pi_" + str(top_neighbour))
		
		#bottom neighbour will have address NETWORK_COLS*y + x
		bottom_neighbour = NETWORK_COLS*y + x
		#check if bottom_neighbour exists
		if y < NETWORK_ROWS:
			#Register the bottom neighbour of this node
			ip_address = BASE_IP_STR + str(bottom_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge("Pi_" + str(this_node), "Pi_" + str(bottom_neighbour))
		
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
"""
for neighbour in connections_list[THIS_NODE-1]:
		#print "java NetworkAdvertise Pi_" + str(THIS_NODE)  + " " + str(neighbour)
		print "while true; do java NetworkAdvertise Pi_" + str(THIS_NODE)  + " " + str(neighbour) + "; sleep 15; done &"
"""

nx_route = nx.shortest_path(network_graph, source="Pi_"+str(THIS_NODE), target="Pi_"+str(DEST_NODE))
#print nx_route

#print nx_route in a form usable by TextSendMultiHop
for node in nx_route:
	sys.stdout.write(node)
	sys.stdout.write(" ")
