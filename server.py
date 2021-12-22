import socket
import random
#return a random question and its answer
def QuestionGenerator():
#returns a tuple of (question str,answer-int)
     n1=random.randint(-20,20)
     n2=random.randint(-20,20)
     return (n1+n2,str(n1)+"+"+str(n2)+"?")     


ip="127.0.0.1"
port=1234
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)#number of clients?
while True:
     client, adress=server.accept()
     print("connection established!")
     answer,question=QuestionGenerator()
     client.send(bytes(question,"utf-8"))
     question=client.recv(2048)
     question=question.decode("utf-8")
     print(question)     
     print(str(answer)==question)