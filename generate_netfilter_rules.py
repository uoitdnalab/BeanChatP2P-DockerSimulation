#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python generate_netfilter_rules.py ROWS COLS

For a rectangular networks of ROWS rows and COLS columns generates the
commands needed for configuring packet routing for simulating the
wireless network.
"""

import sys

import networkx as nx

NETWORK_ROWS = int(sys.argv[1])
NETWORK_COLS = int(sys.argv[2])
BASE_IP_STR = "172.18.1."

def derive_mac(node_id):
	BASE_MAC = '02:42:ac:'
	#Convert node_id into HEX
	padded_hex = format(node_id, '06x')
	derived_addr = BASE_MAC + padded_hex[0:2] + ":" + padded_hex[2:4] + ":" + padded_hex[4:6]
	return str(derived_addr)

#Generate the network graph
connections_list = []
network_graph = nx.Graph()
for y in range(1, NETWORK_ROWS+1):
	for x in range(1, NETWORK_COLS+1):
		
		#Create this node on the nx graph
		this_node = NETWORK_COLS*(y-1) + x
		network_graph.add_node(this_node)
		
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
			network_graph.add_edge(this_node, left_neighbour)
		
		#right neighbour will have address NETWORK_COLS*(y-1) + x + 1
		right_neighbour = NETWORK_COLS*(y-1) + x + 1
		#check if right_neighbour exists
		if x + 1 <= NETWORK_COLS:
			#Register the right neighbour of this node
			ip_address = BASE_IP_STR + str(right_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge(this_node, right_neighbour)
		
		#top neighbour will have address NETWORK_COLS*(y-2) + x
		top_neighbour = NETWORK_COLS*(y-2) + x
		#check if top_neighbour exists
		if y > 1:
			#Register the top neighbour of this node
			ip_address = BASE_IP_STR + str(top_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge(this_node, top_neighbour)
		
		#bottom neighbour will have address NETWORK_COLS*y + x
		bottom_neighbour = NETWORK_COLS*y + x
		#check if bottom_neighbour exists
		if y < NETWORK_ROWS:
			#Register the bottom neighbour of this node
			ip_address = BASE_IP_STR + str(bottom_neighbour)
			neighbour_list.append(ip_address)
			#Also add it to the nx graph
			network_graph.add_edge(this_node, bottom_neighbour)
		
		#Register all connections for this node
		connections_list.append(neighbour_list)



"""
In the wireless network, when a node transmits a packet, all neighboring
nodes receive it regardless of whether or not the packet is intended for
it.
"""
apply_commands = []
remove_commands = []

#For all nodes...
for tx_node in network_graph.nodes():
	#For all neighbors of this node...
	for nbr in network_graph.neighbors(tx_node):
		#If packet originates from tx_node, but is not destined for nbr, send it anyways to other neighbors
		for oth in network_graph.neighbors(tx_node):
			if oth == nbr:
				continue
			add_cmd = "sudo iptables -t mangle -A PREROUTING -m limit --limit 10/s -s " + str(BASE_IP_STR) + str(tx_node) + " -d " + str(BASE_IP_STR) + str(nbr) + " -j TEE --gateway " + str(BASE_IP_STR) + str(oth)
			del_cmd = "sudo iptables -t mangle -D PREROUTING -m limit --limit 10/s -s " + str(BASE_IP_STR) + str(tx_node) + " -d " + str(BASE_IP_STR) + str(nbr) + " -j TEE --gateway " + str(BASE_IP_STR) + str(oth)
			apply_commands.append(add_cmd)
			remove_commands.append(del_cmd)



#Display commands, and write them to files
f_apply = open('apply_netfilter_rules.sh', 'w')
for cmd in apply_commands:
	f_apply.write(cmd)
	f_apply.write('\n')
	print cmd
f_apply.close()

print ""
print "-----------------------------------------------"
print ""

f_remove = open('remove_netfilter_rules.sh', 'w')
for cmd in remove_commands:
	f_remove.write(cmd)
	f_remove.write('\n')
	print cmd
f_remove.close()
