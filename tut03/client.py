# Name: Piyush Singh
# Roll: 2001CS51
# client.py


'''
Client which requests for an expression to be evaluated.
Asks user after each request, whether they want to continue.
'''

import socket
import sys

BUFFER_SIZE = 4096

def Main():
    n = len(sys.argv)
    if n != 3:
        print(f'Exactly Two arguments expected, {n-1} passed. Terminating')
        return
    
    global host, port
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    if host == 'localhost':
        host = '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # If connection refused, the server might be busy or the socket may not exist at the given (IP, Port)
    try:
        s.connect((host, port))
    except Exception as e:
        if type(e) == ConnectionRefusedError:
            print(f"Connection Refused.\nThe server may be busy at the moment.\nPlease try again later.")
        exit(1)
    
    while True:
        msg = input("Enter the expression that you want to be evaluated: ")
        s.send(msg.encode('utf-8'))
        data = s.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
        print(f"The server replied: {data}\n")
        
        to_exit = False
        while True:
            to_continue = input("Do you want to continue[Y/n]: ")
            if to_continue.lower() == 'n':
                to_exit = True
                break
            elif to_continue.lower() == 'y':
                break
            else:
                print(f'Invalid Input. Enter again')
        if to_exit:
            break
    s.close()

if __name__ == '__main__':
    Main()