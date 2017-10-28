#!/bin/sh


#Start the java TextServer, in background
java TextServer SecondPi &

sleep 10

#Start MultiThreadedRx, in background
java MultiThreadedRx &

sleep 10

#NetworkAdvertise this node
#java NetworkAdvertise SecondPi 172.18.1.1
#java NetworkAdvertise SecondPi 172.18.1.3
while true; do java NetworkAdvertise SecondPi 172.18.1.1; sleep 15; done &
while true; do java NetworkAdvertise SecondPi 172.18.1.3; sleep 15; done &

sleep 10

#Start websockify, in background
python /usr/src/websockify/websockify.py 8001 127.0.0.1:9998 &

sleep 10

#Start the simple Python HTTP server
cd BeanChatPortableApp
python -m SimpleHTTPServer 8000
cd ..
