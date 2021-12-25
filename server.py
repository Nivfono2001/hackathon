import socket
import random
import threading
import time
FORMAT="utf-8"
#return a random question and its answer
def QuestionGenerator():
#returns a tuple of (question str,answer-int)
     n1=random.randint(-20,20)
     n2=random.randint(-20,20)
     return (n1+n2,str(n1)+"+"+str(n2)+"?")   

#def countdown(t):
#    while t:
#        mins, secs = divmod(t, 60)
#        timer = '{:02d}:{:02d}'.format(mins, secs)
#        print(timer, end="\r")
#        time.sleep(1)
#        t -= 1
         
def handleClient(client,adress):
     true_answer,ans_from_client="",""
     ctr=0     
     while(str(true_answer)==ans_from_client):  
          print(thread.getName())
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

  
ip=socket.gethostbyname(socket.gethostname())
port=1234
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(2)#number of clients?
while(True):
     client, adress=server.accept()
     thread=threading.Thread(target=handleClient, args=(client,adress))
     print("connection established!")
     thread.start()
     thread.join()     


     