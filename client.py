import socket
import struct
import time
import binascii



MCAST_GRP = '224.1.1.1'
MCAST_PORT = 13117
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
print("here"+str(1))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#defining broadcast
print("here"+str(2))

sock.bind(('', MCAST_PORT))
print("here"+str(3))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
print("here"+str(4))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print("here"+str(5))
TCP_PORT=struct.unpack('LBh',sock.recv(1024))[2]
print("CONNECTING TO"+str(TCP_PORT))
ip=socket.gethostbyname(socket.gethostname())
port=TCP_PORT
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip,port))
print("Game Started!")
isTrue=True
myname="UNICORNS/TCPICKACHU(SHEM ZMANI)\n"
server.send(bytes(myname,"utf-8"))
while(isTrue):
    question=server.recv(2048)
    question=question.decode("utf-8")
    print(question)
    answer=input("Enter answer:")
    server.send(bytes(answer,"utf-8"))
    isTrue=server.recv(2048)
    isTrue=bool(isTrue.decode("utf-8"))
    print(isTrue)
total_score=server.recv(2048)
total_score=total_score.decode("utf-8")
print(question)  













# UDP_IP = "127.0.0.1"
# UDP_PORT = 13117
# while True: 
#     sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) # UDP
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     sock.bind(('', UDP_PORT))#RECIEVING FROM ALL INTERFACES
#     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#     data=int(data)
#     print("port is: %s" % data)
#     time.sleep(2)
    

  