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
     print(thread.getName())
     name_of_client=client.recv(2048)
     print("welcome:"+str(name_of_client.decode("utf-8")))
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
     group = '224.1.1.1'
     port = 1234
     # 2-hop restriction in network
     ttl = 2
     sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM,
                     socket.IPPROTO_UDP)
     sock.setsockopt(socket.IPPROTO_IP,
                socket.IP_MULTICAST_TTL,
                ttl)

     udp_packet=struct.pack('LBh',0xabcddcba,0x2,port)    
            
     while STOP_BROADCAST:
          sock.sendto(udp_packet, (group, 13117))
          time.sleep(1)
          print("sending again")   
global STOP_BROADCAST
STOP_BROADCAST=True
TCP_PORT=1234
MYPORT = 13117
udp_thread=threading.Thread(target=Broadcasting)
udp_thread.start()
ip=socket.gethostbyname(socket.gethostname())
port=1234
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(2)#number of clients?
max_Client=2
connected_Clients=0
while connected_Clients<max_Client:
     client, adress=server.accept()
     connected_Clients+=1
     thread=threading.Thread(target=handleClient, args=(client,adress))
     print("connection established: number of clients:"+str(connected_Clients))
     thread.start()
STOP_BROADCAST=False
  
 
     







# def Broadcasting():
#      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#      s.bind(('', 5555))
#      s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#      while 1:
#           # first_part=0xabcddcba+0x2
#           data =TCP_PORT
#           s.sendto(bytes(str(data),FORMAT), ('255.255.255.255', MYPORT))
#           time.sleep(2)


# TCP_PORT=1234
# MYPORT = 13117
# udp_thread=threading.Thread(target=Broadcasting)
# udp_thread.start()
# ip=socket.gethostbyname(socket.gethostname())
# port=1234
# server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((ip,port))
# server.listen(2)#number of clients?
# ctr=0
# while(True):
#      if ctr<2:
#           client, adress=server.accept()
#           ctr+=1
#      #thread=threading.Thread(target=handleClient, args=(client,adress))
#      print("connection established!")



     





# UDP_IP = "127.0.0.1"
# UDP_PORT = 13117
# MESSAGE = b"Please Enter Our Game!!!!"
 
# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
# print("message: %s" % MESSAGE)

#      sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) # UDP
#      sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))  
#      time.sleep(2)
#      print(i)

