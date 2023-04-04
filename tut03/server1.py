# Name: Piyush Singh
# Roll: 2001CS51
# server1.py

'''
Server which evaluates the expression requested by the client
Handles only one client at a time. 
'''

import socket
import sys

BUFFER_SIZE = 4096
n_clients = 1

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
    
    # Server may not by able to bind if (IP, Port) is invalid
    try:
        server_socket.bind((host, port))
    except Exception as e:
        if type(e) == PermissionError:
            print("Permission Denied for the given port. Use a higher port number. Terminating")
        else:
            print("Invalid IP address or Port Number. Not able to bind.\nTerminating")
        return
    server_socket.listen(n_clients)

    print(f'Listening on port {port}')
    
    client_socket, client_addr = server_socket.accept()
    print(f'Connection established with {client_addr[0]} at port {client_addr[1]}')
    
    # Keep listening on the given (IP, Port) and accept connection from a single client.
    while True:
        # Server closes the socket to prevent further connections.
        server_socket.close()
        data = client_socket.recv(BUFFER_SIZE)
        data = str(data.decode('utf-8'))
        if data:
            print(f'The client {client_addr[1]} sent: {data}')
        if not data:
            print(f'Connection closed with {client_addr[0]} at port {client_addr[1]}')

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(n_clients)
            
            client_socket, client_addr = server_socket.accept()
            print(f'Connection established with {client_addr[0]} at port {client_addr[1]}')
            continue
        try:
            data = str(eval(data))
        except:
            data = 'Invalid Syntax'
        print(f'Sending response: {data}')
        data = data.encode('utf-8')
        client_socket.send(data)
            

if __name__ == '__main__':
    Main()