from socket import *
import time

ctrCmd = ["INC", "DECR", "STOP", "DIR"]

HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

PORT = 21566
ADDR = (HOST,PORT)
tcpSerSock_send = socket(AF_INET, SOCK_STREAM)
tcpSerSock_send.bind(ADDR)
tcpSerSock_send.listen(5)

while True:
        print('Waiting for connection')
        tcpCliSock,addr = tcpSerSock.accept()
        tcpSerSock_send,addr = tcpSerSock_send.accept()
        print('...connected from : ' + str(addr))
        try:
            while True:
                    data = ''
                    data = tcpCliSock.recv(BUFSIZE)

                    if not data:
                            break

                    command = str(data.decode("utf-8"));
                    print("Command from android: --" + command + "--")

                    if command == "INC":
                            print("Increase")
                            data_send = "holaaa"
                            tcpSerSock_send.send(data_send.encode())
                            data_end = "\n"
                            tcpSerSock_send.send(data_end.encode())
                            # GPIO.output(26,GPIO.HIGH)
                    elif command == "DECR":
                            print("Decrease")
                            # GPIO.output(26,GPIO.LOW)
                    elif command == "STOP":
                            print("STOP")
                            # GPIO.output(26,GPIO.LOW)
                    elif command == "DIR":
                            print("CHANGE DIR")
                            # GPIO.output(26,GPIO.LOW)

        except KeyboardInterrupt:
                # GPIO.cleanup()
                print("Interrupt")
tcpSerSock.close();
