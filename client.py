import socket
ip="127.0.0.1"
port=1234
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip,port))
print("yeeyyyyy we succeeded!!!")
question=server.recv(2048)
question=question.decode("utf-8")
print(question)
answer=input("Enter answer")
server.send(bytes(answer,"utf-8"))