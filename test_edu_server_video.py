import socket
import struct
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from picamera2.encoders import Quality
from _thread import *
from threading import Thread
from threading import Condition
import io
import fcntl

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class Server:
    def __init__(self):
        self.tcp_Flag = True
        self.endChar='\n'
        self.intervalChar='#'

    def get_interface_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 'sll_protocol')
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                            0x8915,
                                            struct.pack('256s',b'wlan0'[:15])
                                            )[20:24])
    def StartTcpServer(self):
        HOST=str("192.168.4.40")
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket.bind((HOST, 8000))
        self.server_socket.listen(1)
        print('Server address: '+HOST)
    def StopTcpServer(self):
        try:
            self.connection.close()
            self.connection1.close()
        except Exception as e:
            print ('\n'+"No client connection")
    def Reset(self):
        self.StopTcpServer()
        self.StartTcpServer()
        # self.SendVideo=Thread(target=self.sendvideo)
        self.ReadData=Thread(target=self.readdata)
        # self.SendVideo.start()
        self.ReadData.start()

    def sendvideo(self):
        try:
            self.connection,self.client_address = self.server_socket.accept()
            self.connection=self.connection.makefile('wb')
        except:
            pass
        self.server_socket.close()
        print ("socket video connected ... ")
        camera = Picamera2()
        camera.configure(camera.create_video_configuration(main={"size": (400, 300)}))
        output = StreamingOutput()
        encoder = JpegEncoder(q=90)
        camera.start_recording(encoder, FileOutput(output),quality=Quality.VERY_HIGH)
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            try:
                lenFrame = len(output.frame)
                #print("output .length:",lenFrame)
                lengthBin = struct.pack('<I', lenFrame)
                self.connection.write(lengthBin)
                self.connection.write(frame)
            except Exception as e:
                camera.stop_recording()
                camera.close()
                print ("End transmit ... " )
                break

try:
    TCP_Server=Server()
    TCP_Server.StartTcpServer()
    SendVideo=Thread(target=TCP_Server.sendvideo)
    SendVideo.start()

    while True:
        pass
except KeyboardInterrupt:
        try:
            stop_thread(SendVideo)
            print ("Close TCP")

        except:
            pass
        try:
            TCP_Server.server_socket.shutdown(2)
            TCP_Server.StopTcpServer()

        except:
            pass
