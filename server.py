from ctypes import addressof
import socket
import random
import threading
import time
import struct
FORMAT="utf-8"

#unicorn photo file
with open('unicorn.txt', 'r') as file:
    unicorn_paint = file.read()

#return a random question and its answer - (answer, question)
def QuestionGenerator():
     n1=random.randint(0,4)
     n2=random.randint(0,4)
     return n1+n2, str(n1)+"+"+str(n2)+"?"

def handleClient(client, address,true_answer, question):
     print("I am thread number: "+ str(thread.name))
     name_of_client=client.recv(2048)
     name_of_client=name_of_client.decode("utf-8")

     #critical section - for adding the current player name to the list of names
     #NAMES - is a list of tuples: (client name, thread number)
     NAME_MUTEX.acquire()
     NAMES.append((name_of_client, thread.name))
     NAME_MUTEX.release()
     #end of critical section
     #busy wait - the client waits the game to begin
     while(WAIT_FOR_START):
          pass
     #game starts
     s1 = "Welcome to the Quick Maths game of the UNICORNS\n "
     welcome =s1 +'\n'+ unicorn_paint +'\n'+ "1. "+ str(NAMES[0]) + '\n'+ "2. " + str(NAMES[1]) +'\n' + "Answer the next question as fast as you can:" + '\n'+ str(question)
     client.send(bytes(welcome,"utf-8"))
     ans_from_client=client.recv(2048)

     #critical section - the moment one of the players answers:
     ANSWER_MUTEX.acquire()
     ANSWERS.append(ans_from_client.decode("utf-8"))
     #current player answered correctly - he wins.
     if (ANSWERS[0] == str(true_answer)):
          WINNERS.append(name_of_client)
     else: #current player was wrong - the other player wins.
          for name in NAMES:
               if name[0] != str(name_of_client):
                    WINNERS.append(name[0])
                    break
     print(WINNERS)               
     game_over = "Game over!\n " + "The winner is: " + str(WINNERS[0]) 
     print("Game over!\n " + "The winner is: " + str(WINNERS[0]))
     client.send(bytes(game_over,"utf-8"))
     
     ANSWER_MUTEX.release()
     client.close()
     global STOP_BROADCAST
     STOP_BROADCAST=True


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








ALIVE=True
while(ALIVE):
     #argument definition and initialization
     global STOP_BROADCAST
     STOP_BROADCAST=True
     SERVER_IP=socket.gethostbyname(socket.gethostname())
     TCP_PORT=1234
     global WAIT_FOR_START
     WAIT_FOR_START = True
     global NAMES
     NAMES = []
     global NAME_MUTEX
     NAME_MUTEX = threading.Lock()
     global ANSWERS
     global WINNERS
     ANSWERS = []
     WINNERS = []
     ANSWER_MUTEX = threading.Lock()

     #starting sending offers
     udp_thread=threading.Thread(target=Broadcasting)
     udp_thread.start()

     #TCP connection establishment
     server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_socket.bind((SERVER_IP,TCP_PORT))
     server_socket.listen()#number of clients?
     max_Client=2
     connected_Clients=0
     true_answer, question=QuestionGenerator()
     print(true_answer)
     print(question)
     while connected_Clients<max_Client:
          client, adress=server_socket.accept()
          connected_Clients+=1
          thread=threading.Thread(target=handleClient, args=(client,adress, true_answer, question))
          print("connection established: number of clients:"+str(connected_Clients))
          thread.start()
     #now we have 2 clients connected to the server
     STOP_BROADCAST=False
     time.sleep(5) #timer for 10 seconds
     WAIT_FOR_START = False
     while(STOP_BROADCAST!=True):
           print("still in here...")
           time.sleep(2)
     print("Game Over, start offering new requests...")