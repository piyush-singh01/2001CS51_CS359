# Name: Piyush Singh
# Roll: 2001CS51
# server2.py

'''
Multithreaded server, which evaluates the expression requested by the client.
Can handle multiple clients concurrently
'''

import socket
import sys
from _thread import*

BUFFER_SIZE = 4096
to_exit = 0
n_client = 40


# A thread which runs for each new client.
def thread_function(client_socket, addr):
    # Keep running until client sends data
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        data = str(data.decode('utf-8'))
        if data:
            print(f'The client {addr[1]} sent: {data}')
        if not data:
            print(f'Connection closed with client {addr[1]}')
            return
        try:
            data = str(eval(data))
        except:
            data = "Invalid Syntax"
        print(f'Sending response {data}')
        data = data.encode('utf-8')
        client_socket.send(data)

def Main():
    n = len(sys.argv)
    if n != 3:
        print(f'Exactly Two arguments expected, {n-1} passed. Terminating')
        return
    
    global host, port

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except Exception as e:
        if type(e) == ValueError:
            print('Invalid Port Number. Terminating')
        return

    if host.lower == 'localhost':
        host = '127.0.0.1'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.bind((host, port))
    except Exception as e:
        if type(e) == PermissionError:
            print("Permission Denied for the given port. Use a higher port number. Terminating")
        else:
            print("Invalid IP address or Port Number. Not able to bind.\nTerminating")
        return
    
    server_socket.listen(n_client)
    print(f'Listening on port {port}')

    # Start a new thread for each new client
    while True:
        client_socket, address = server_socket.accept()
        print(f'Connection established with {address[0]} at {address[1]}')
        start_new_thread(thread_function, (client_socket,address,))

if __name__ == '__main__':
    Main()


