#!/bin/bash

# 	This script will build a network of Docker containers with
#	 NET_ROWS * NET_COLS intermediate (repeater) nodes

EXECUTE_SCRIPT="run_dockers.sh"

NET_ROWS=$1
NET_COLS=$2
N_CONTAINERS=$(echo "$(($NET_ROWS * $NET_COLS))")

#Make EXECUTE_SCRIPT blank
echo -ne '' > $EXECUTE_SCRIPT

#Create a build directory
mkdir __build

#Create the mounts directory
mkdir __mounts

#Initial director
INIT_DIR=$(pwd)

for i in `seq 1 $N_CONTAINERS`;
do
	#Derive it's address
	IP_ADDR="172.18.1.$i"
	echo "--- Building Container $i with IP = $IP_ADDR ---"
	
	#Zero padded container number
	CONTAINER_NUMBER=$(printf "%03d" $i)
	
	#Create a directory for this container
	mkdir __build/container_$CONTAINER_NUMBER
	
	#Make a mountpoint for this container
	mkdir __mounts/container_$CONTAINER_NUMBER
	
	#Copy the base directory
	cp -rf BASE_FILES_AUTO_TEST/* __build/container_$CONTAINER_NUMBER
	
	#Generate run_container_tests.sh
	./build_container_automated_tests.sh __build/container_$CONTAINER_NUMBER/BeanChatP2P/run_container_tests.sh $i $NET_ROWS $NET_COLS
	
	#Generate the modified mesh.js
	cd __build/container_$CONTAINER_NUMBER/BeanChatP2P/BeanChatPortableApp
	
	#...modify the BOOTSTRAP_NODE
	cat mesh.js | sed s/'BOOTSTRAP_NODE = "Pi_1"'/BOOTSTRAP_NODE\ =\ \"Pi_$i\"/ > newmesh.js
	rm mesh.js
	mv newmesh.js mesh.js
	
	#...modify the local websocket port
	cat mesh.js | sed s/"127.0.0.1:8001"/"127.0.0.1:8$CONTAINER_NUMBER"/ > newmesh.js
	rm mesh.js
	mv newmesh.js mesh.js
	
	cd $INIT_DIR
	
	#Docker build
	cd __build/container_$CONTAINER_NUMBER
	docker build -t beanchat-java-app-$CONTAINER_NUMBER .
	#cd ..
	cd $INIT_DIR
	
	#Derive the MAC address for this device
	MAC_ADDR="$(python derive_mac.py $i)"
	
	#Derive the command to start this container, and write to a file
	CMD_START="docker run -v $(pwd)/__mounts/container_$CONTAINER_NUMBER:/usr/src/BeanChatP2P/rx_messages --net beanchatnet --ip 172.18.1.$i --mac-address $MAC_ADDR -it --rm --name my-running-app-$CONTAINER_NUMBER beanchat-java-app-$CONTAINER_NUMBER"
	echo "xterm -e \"$CMD_START\" &" >> $EXECUTE_SCRIPT
	
	echo "--- Completed Container $i ---"
done

#Setup lossy, speed-limited network emulation
echo 'for iface in /sys/class/net/veth*' >> $EXECUTE_SCRIPT
echo 'do' >> $EXECUTE_SCRIPT
echo 'echo "Configuring network interface $(basename $iface)."' >> $EXECUTE_SCRIPT
echo 'sudo tc qdisc add dev $(basename $iface) handle 1: root htb default 11' >> $EXECUTE_SCRIPT
echo 'sudo tc class add dev $(basename $iface) parent 1: classid 1:1 htb rate 1mbps' >> $EXECUTE_SCRIPT
echo 'sudo tc class add dev $(basename $iface) parent 1:1 classid 1:11 htb rate 1mbps' >> $EXECUTE_SCRIPT
echo 'sudo tc qdisc add dev $(basename $iface) root netem loss 3%' >> $EXECUTE_SCRIPT
echo 'done' >> $EXECUTE_SCRIPT

echo "python get_timing_info.py" >> $EXECUTE_SCRIPT

#Make deploy script executable
chmod u+x $EXECUTE_SCRIPT
