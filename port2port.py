import socket
from argparse import ArgumentParser
from threading import Thread


class Port2Port:

    def __init__(self ,listen_port ,remote_port ,listen_ip ,remote_ip):
        self.listen_port = int(listen_port)
        self.remote_port = int(remote_port)
        self.listen_ip = listen_ip
        self.remote_ip = remote_ip

    def start(self):

        print(f'listen ip : {self.listen_ip} listen port : {self.listen_port}')
        print(f'remote ip : {self.remote_ip} remote port : {self.remote_port}')

        while True:
            self.start_listening()

    def start_listening(self):
        '''
        this function starts listening on a port ,for forwarding
        '''

        self.client_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.client_socket.bind((self.listen_ip ,self.listen_port))
        self.client_socket.listen(5)

        try :
            print('Listening for accepting connections ...')
            self.client_conn ,addr = self.client_socket.accept()
            print(f'client connected : {addr[0]}')

        except Exception as e :
            print(f'Error --> {e}')
            self.close_both_connection()

        else:
            self.connect_to_remote_socket()

    def connect_to_remote_socket(self):
        '''
        this function creates remote socket ,for forwarding
        '''

        self.remote_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        try :
            self.remote_socket.connect((self.remote_ip ,self.remote_port))

        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

        else:
            Thread(target=self.forward_to_remote_port).start()
            Thread(target=self.forward_from_remote_port).start()

    def forward_to_remote_port(self):
        try :
            while True :
                client_data = self.client_conn.recv(4096)
                if not client_data :
                    break
                self.remote_socket.sendall(client_data)

        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

    def forward_from_remote_port(self):
        try :
            while True :
                remote_data = self.remote_socket.recv(4096)
                if not remote_data :
                    break
                self.client_conn.sendall(remote_data)

        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

    def close_both_connection(self):
        try :
            self.client_conn.close()
            self.remote_socket.close()
        except Exception as e:
            print(f'Error --> {e}')

def print_help():
    help_msg = '''

usage: port2port.py [-h] [-lp LISTEN_PORT] [-rp REMOTE_PORT] [--listen-ip LISTEN_IP [default : 0.0.0.0]]

arguments:
  --listen-port or -lp LISTEN_PORT (listen port number)
  --remote-port or -rp REMOTE_PORT (remote port to forward)
  
optional arguments :
   --listen-ip or -lip LISTEN_IP (ip address to listen [default : 0.0.0.0])
   --remote-ip or -rip LISTEN_IP (ip address to forward [default : 127.0.0.1])
   
   -h or --help                  (show this help message and exit)
    '''
    print(help_msg)


if __name__ == '__main__':
    parser = ArgumentParser(allow_abbrev=False ,add_help=False)
    parser.add_argument('-lp' ,'--listen-port' ,help='listen port number')
    parser.add_argument('-rp' ,'--remote-port' ,help='remote port to forward')
    parser.add_argument('-lip' ,'--listen-ip' ,help='ip address to listen [default : 0.0.0.0]' ,default='0.0.0.0')
    parser.add_argument('-rip', '--remote-ip', help='ip address to forward [default : 127.0.0.1]', default='127.0.0.1')
    args ,unknown = parser.parse_known_args()

    if (args.listen_port) and (args.remote_port):
        port2port = Port2Port(args.listen_port ,args.remote_port ,args.listen_ip ,args.remote_ip)
        port2port.start()
    else:
        print_help()
