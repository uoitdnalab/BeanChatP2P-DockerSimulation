FROM openjdk:7
COPY BeanChatP2P /usr/src/BeanChatP2P
COPY websockify /usr/src/websockify
WORKDIR /usr/src/BeanChatP2P/
RUN javac -cp json-simple-1.1.1.jar *.java
CMD ["bash", "run_container_tests.sh"]
