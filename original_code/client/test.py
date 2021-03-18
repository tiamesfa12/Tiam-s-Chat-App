from client import Client
import time
from threading import Thread


c1 = Client("Tiam")
c2 = Client("Tirito")

def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1) # updates every 0.1 seconds
        new_messages = c1.get_messages() # get new messages from client
        msgs.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()


c1.send_message("Howdy")
time.sleep(5)
c2.send_message("whats up")
time.sleep(5)
c1.send_message("nothing much, hbu")
time.sleep(5)
c2.send_message("Im bored")
time.sleep(4)

c1.disconnect()
time.sleep(2)
c2.disconnect()

