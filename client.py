import socket
import struct
import time
import binascii


port = 13117

#UDP conversation with a random server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#defining broadcast
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)#defining broadcast

sock.bind(('', port))
first_pack,server_address=sock.recvfrom(1024)
print("Recieved offer from "+ str(server_address[0])+" , attempting to connect...")

#connetion to server in TCP protocol
TCP_PORT=struct.unpack('LBh', first_pack)[2]
#print("CONNECTING TO"+str(TCP_PORT))
ip=socket.gethostbyname(socket.gethostname())
port=TCP_PORT
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))
#print("Game Started!")
isTrue=True
myname="UNICORNS\n"
print("The winner team AKA the Unicorns client started, waiting for your offers...")
server.send(bytes(myname,"utf-8"))

#playing the game
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

  