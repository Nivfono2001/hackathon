from ctypes import addressof
import socket
import random
import threading
import time
import struct
import scapy.all
FORMAT = "utf-8"

# unicorn photo file
with open('unicorn.txt', 'r') as file:
    unicorn_paint = file.read()
    unicorn_paint="\033[1;35;40m"+unicorn_paint

# return a random question and its answer - (answer, question)
def QuestionGenerator():
    n1 = random.randint(0, 4)
    n2 = random.randint(0, 4)
    retval = str(n1) + "+" + str(n2) + "?"
    question_bank = {}  # dictionary of question:answer
    question_bank['Yossi is leacturer number?'] = 1
    question_bank['How many horns does unicorn has?'] = 1
    question_bank['which Corona wave starts now?'] = 5
    question_bank['How many `Humshey TORA` there are?'] = 5
    question_bank['How many colors there are in the rainbow spectrum?'] = 7
    if random.randint(0, 10) > 7:
        keys = list(question_bank.keys())
        numkey = random.randint(0, len(keys) - 1)
        return question_bank[keys[numkey]], keys[numkey]
    return n1 + n2, retval

#editing the IP address
def edit_ip(curr_ip):
    l=curr_ip.split(".")
    return l[0]+"."+l[1]+"."+"255.255"


def handleClient(client, address, true_answer, question):
    # print("I am thread number: "+ str(thread.name))
    name_of_client = client.recv(2048)
    name_of_client = name_of_client.decode("utf-8")
    print("client is:" +str(name_of_client))
    # critical section - for adding the current player name to the list of names
    # NAMES - is a list of tuples: (client name, thread number)
    NAME_MUTEX.acquire()
    NAMES.append((name_of_client, thread.name))
    NAME_MUTEX.release()
    # end of critical section
    # busy wait - the client waits the game to begin
    while (WAIT_FOR_START):
        time.sleep(2)
    # game starts
    s1 = "Welcome to the Quick Maths game of the UNICORNS\n"
    print(s1)
    welcome = s1 + '\n' + unicorn_paint + '\n' + "1. " + str(NAMES[0][0]) + '\n' + "2. " + str(
        NAMES[1][0]) + '\n' + "Answer the next question as fast as you can:" + '\n' + str(question)
    client.send(bytes(welcome, "utf-8"))
    try:
        client.settimeout(10)
        ans_from_client = client.recv(2048)
        # critical section - the moment one of the players answers:
        ANSWER_MUTEX.acquire()
        ANSWERS.append(ans_from_client.decode("utf-8"))
        # current player answered correctly - he wins.
        if (ANSWERS[0] == str(true_answer)):
            WINNERS.append(name_of_client)
        else:  # current player was wrong - the other player wins.
            for name in NAMES:
                if name[0] != str(name_of_client):
                    WINNERS.append(name[0])
                    break
        game_over = "Game over!\n " + "The winner is: " + str(WINNERS[0])
        print("Game over!\n " + "The winner is: " + str(WINNERS[0]))
        client.send(bytes(game_over, "utf-8"))
        ANSWER_MUTEX.release()
        client.close()
    except:
        print("client run out of time")
        try:
            if len(WINNERS) == 0:
                game_over = "Game over!\n " + "It's a tie!"
                client.send(bytes(game_over, "utf-8"))
                print(game_over)
                client.close()
            else:
                game_over = "Game over!\n " + "The winner is: " + str(WINNERS[0])
                print("Game over!\n " + "The winner is: " + str(WINNERS[0]))
                client.send(bytes(game_over, "utf-8"))
                client.close()

        except:
            print("timer stoped before end")
        
        global STOP_BROADCAST
        STOP_BROADCAST = True


def Broadcasting():
    address = scapy.all.get_if_addr('eth2')
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM,
                         socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    TCP_PORT = 2019
    udp_packet = struct.pack('IbH', 0xabcddcba, 0x2, TCP_PORT)
    print("UNICORN server started, listening on IP address: " + str(address))
    print(address)
    while STOP_BROADCAST:
        sock.sendto(udp_packet, (edit_ip(address), 13188))
        time.sleep(1)

#### Main Thread ####
ALIVE = True
while (ALIVE):
    # argument definition and initialization
    global STOP_BROADCAST
    STOP_BROADCAST = True
    SERVER_IP =address = scapy.all.get_if_addr('eth2')
    global STOP_THREADS
    STOP_THREADS = False
    global TCP_PORT
    TCP_PORT = 2019
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

    # starting sending offers
    udp_thread = threading.Thread(target=Broadcasting)
    udp_thread.start()

    # TCP connection establishment
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, TCP_PORT))
    server_socket.listen()  # number of clients?
    max_Client = 2
    connected_Clients = 0
    true_answer, question = QuestionGenerator()
    print(true_answer)
    print(question)
    while connected_Clients < max_Client:
        client, adress = server_socket.accept()
        connected_Clients += 1
        thread = threading.Thread(target=handleClient, args=(client, adress, true_answer, question))
        print("connection established: number of clients:" + str(connected_Clients))
        thread.start()
    # now we have 2 clients connected to the server
    STOP_BROADCAST = False
    time.sleep(10)  # timer for 10 seconds
    #now we can start the game
    WAIT_FOR_START = False
    while (STOP_BROADCAST != True):
        print("still in here...")
        time.sleep(3)
    thread.join()

    print("Game Over, start offering new requests...")
