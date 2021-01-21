import socket, sys
from multiprocessing import Pool
BUFFER_SIZE = 4096
port = 80
payload = f'GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n'

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    with Pool() as p:
        address = [("127.0.0.1", 8001)]
        p.map(make_request, address * 10)        
        
def make_request(address):
    #make the socket and connect
    s = create_tcp_socket()
    s.connect(address)
    #send the data and shutdown
    send_data(s, payload)
    s.shutdown(socket.SHUT_WR)

    #continue accepting data until no more left
    full_data = b""
    while True:
        data = s.recv(BUFFER_SIZE)
        if not data:
                break
        full_data += data
    print(full_data)
    s.close()
    return s

if __name__ == "__main__":
    main()