OUTPUT_FILE=$1
NODE_ID=$2
NET_ROWS=$3
NET_COLS=$4

echo "#!/bin/bash" > $OUTPUT_FILE

echo "#Start the java TextServer, in background" >> $OUTPUT_FILE
echo "java TextServer Pi_$NODE_ID | python get_messages_from_log.py &" >> $OUTPUT_FILE

echo "sleep 10" >> $OUTPUT_FILE

echo "#Start MultiThreadedRx, in background" >> $OUTPUT_FILE
echo "java MultiThreadedRx &" >> $OUTPUT_FILE

echo "sleep 10" >> $OUTPUT_FILE

echo "#NetworkAdvertise this node" >> $OUTPUT_FILE
#Figure out which nodes this should advertise to based on network topology
python generate_network_advertisements.py $NET_ROWS $NET_COLS $NODE_ID  >> $OUTPUT_FILE


echo "sleep 90" >> $OUTPUT_FILE

#Do send all messages from this node, but in a random order
./generate_test_messages.sh 100 $NODE_ID $NET_ROWS $NET_COLS | shuf >> $OUTPUT_FILE

echo "#Start websockify, in background" >> $OUTPUT_FILE
echo "python /usr/src/websockify/websockify.py 8001 127.0.0.1:9998 &" >> $OUTPUT_FILE

echo "sleep 10" >> $OUTPUT_FILE

echo "#Start the simple Python HTTP server" >> $OUTPUT_FILE
echo "cd BeanChatPortableApp" >> $OUTPUT_FILE
echo "python -m SimpleHTTPServer 8000" >> $OUTPUT_FILE
echo "cd .." >> $OUTPUT_FILE

