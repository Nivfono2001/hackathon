import socket
import struct
import threading
import time
import binascii


# def HandleInputFromKeyBoard(server):
#     answer=input("Enter answer:")
#     server.send(bytes(answer,"utf-8"))
     




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
ip=socket.gethostbyname(socket.gethostname())
port=TCP_PORT
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))
isTrue=True
myname="UNICORNS\n"
id=input("enter id")
print("The winner team AKA the Unicorns client started, waiting for your offers...")
server.send(bytes(myname+str(id),"utf-8"))#sending name

#playing the game
question=server.recv(2048)
question=question.decode("utf-8")
print(question)#recieving question
#thread=threading.Thread(target=HandleInputFromKeyBoard,args=(server))
answer=input("Enter answer:")
server.send(bytes(answer,"utf-8"))
     
results = server.recv(2048)
results = results.decode("utf-8")
print(results)   



