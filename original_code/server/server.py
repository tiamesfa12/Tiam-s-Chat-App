from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

#Global constants
HOST = 'localhost'
PORT = 5500
BUFSIZ = 512 # how big the messages are going to be
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10 # the max number of connections allowed
#global variables
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # setup the server

def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(person):
    """
    Thread to handle every message from the client
    :param person: Person
    :return: None
    """
    client = person.client

    # first message received is always the persons name
    name = client.recv(BUFSIZ).decode("utf8")
    client.set_name(name)
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "") # broadcast welcome message

    while True: # wait for messages that comes from the person
        try:
            msg = client.recv(BUFSIZ)

            if msg != bytes("{quit}", "utf8"): # if message is quit disconnect
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else: # send message to all remaining clients
                broadcast(msg, name+": ")
        except Exception as e:
            print("[EXCEPTION]", e)
            break



def wait_for_connection():
    """
    Wait to retrieve connection from the new client, start a new thread once you have connected
    :param SERVER: SOCKET
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept() # wait for any new connections
            person = Person(addr, client) # create a new person for connections
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break
    print("Server has crashed")




if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # listen for connections
    print("[STARTED] Waiting for a connection..... Please hold")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
