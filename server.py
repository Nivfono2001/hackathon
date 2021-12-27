from ctypes import addressof
import socket
import random
import threading
import time
import struct
FORMAT="utf-8"

#return a random question and its answer
def QuestionGenerator():
     #returns a tuple of (question str,answer-int)
     n1=random.randint(-20,20)
     n2=random.randint(-20,20)
     return (n1+n2,str(n1)+"+"+str(n2)+"?")   
     
def handleClient(client,adress):
     true_answer,ans_from_client="",""
     ctr=0     
     #print(thread.getName())
     while(WAIT_FOR_START):
          pass
     name_of_client=client.recv(2048)
     print("Welcome to Quick Maths. "+str(name_of_client.decode("utf-8")))
     while(str(true_answer)==ans_from_client):  
          true_answer,question=QuestionGenerator()
          client.send(bytes(question,"utf-8"))
          ans_from_client=client.recv(2048)
          ans_from_client=ans_from_client.decode("utf-8")
          print(ans_from_client)
          print(str(true_answer)==ans_from_client)
          client.send(bytes(str(str(true_answer)==ans_from_client),FORMAT))
          ctr+=1
     ctr-=1          
     client.send(bytes("total score:"+str(ctr),FORMAT))     
     client.close()

def Broadcasting():
     address = socket.gethostbyname(socket.gethostname())
     # 2-hop restriction in network
     ttl = 2
     sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM,
                     socket.IPPROTO_UDP)
     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

     udp_packet=struct.pack('LBh',0xabcddcba,0x2,TCP_PORT)    
     print("UNICORN server started, listening on IP address: "+ str(address))
     while STOP_BROADCAST:
          sock.sendto(udp_packet, ('<broadcast>', 13117))
          time.sleep(1)
          print("sending again")#delete in the end

#argument definition and initialization
global STOP_BROADCAST
STOP_BROADCAST=True
SERVER_IP=socket.gethostbyname(socket.gethostname())
TCP_PORT=1234
global WAIT_FOR_START
WAIT_FOR_START = True

#starting sending offers
udp_thread=threading.Thread(target=Broadcasting)
udp_thread.start()

#TCP connection establishment
server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP,TCP_PORT))
server_socket.listen()#number of clients?
max_Client=2
connected_Clients=0
while connected_Clients<max_Client:
     client, adress=server_socket.accept()
     connected_Clients+=1
     thread=threading.Thread(target=handleClient, args=(client,adress))
     print("connection established: number of clients:"+str(connected_Clients))
     thread.start()
#now we have 2 clients connected to the server
STOP_BROADCAST=False
time.sleep(2) #timer for 10 seconds
WAIT_FOR_START = False
