#!/bin/bash

#	Generates N test text-messages each 128 chars long and prepares them
#	to be sent to all nodes except NODE_ID

N=$1
NODE_ID=$2
NETWORK_ROWS=$3
NETWORK_COLS=$4
TOTAL_NODES=$(echo "$(($NETWORK_ROWS * $NETWORK_COLS))")

for dest in `seq 1 $TOTAL_NODES`
do
	if [ $dest -eq $NODE_ID ]
	then
		continue
	fi
	
	#Find the path from source to destination
	src=$NODE_ID
	graph_route=$(python generate_graph_route.py $NETWORK_ROWS $NETWORK_COLS $dest $src)
	
	#TEMPFILE=$(mktemp)
	for i in `seq 1 $N`;
	do
		#Generate the random message contents
		msg=$(cat /dev/urandom | head -c 8192 | sha512sum - | cut -d ' ' -f1 | head -c 128)
		
		#Find the path from source to destination
		#src=$NODE_ID
		#graph_route=$(python generate_graph_route.py $NETWORK_ROWS $NETWORK_COLS $dest $src)
		
		#Generate the command to send this message
		#java TextSendMultiHop MESSAGE DST ... k ... k+1 ... SRC
		
		
		echo "java TextSendMultiHop \"Pi_$src $msg\" $graph_route"
		#echo "java TextSendMultiHop \"Pi_$src $msg\" $graph_route" >> TEMPFILE
	done
	#Shuffle message send commands
	#cat $TEMPFILE | shuf
	#rm $TEMPFILE
done
