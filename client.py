import socket
ip=socket.gethostbyname(socket.gethostname())
port=1234
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip,port))
print("Game Started!")
isTrue=True
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