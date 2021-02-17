# Port2Port
**port2port** forwards two sockets data to each other. 

It's useful when : 
- You can not or don't want to connect to your target directly.
- You can not connect to remote port because firewall is blocking a port on 0.0.0.0 ,but you can connect to that port with `loopback` IP address.

Installation
----
    git clone https://github.com/nxenon/port2port.git
    cd port2port

Usage
---
    sudo python3 port2port.py --listen-ip 0.0.0.0 --listen-port 5678 --remote-ip 192.168.1.1 --remote-port 23
    then connect to port 5678 to start forwarding

optional arguments :

--service SERVICE_NAME (Determine Service)

valid services :
- http

like :

    sudo python3 port2port.py --listen-ip 0.0.0.0 --listen-port 5678 --remote-ip 192.168.1.1 --remote-port 80 --service http


Help
----
    usage: port2port.py [-h] [-lp LISTEN_PORT] [-rp REMOTE_PORT] [--listen-ip LISTEN_IP [default : 0.0.0.0]]

    arguments:
        --listen-port or -lp LISTEN_PORT (listen port number)
        --remote-port or -rp REMOTE_PORT (remote port to forward)
  
    optional arguments :
        --listen-ip or -lip LISTEN_IP (ip address to listen [default : 0.0.0.0])
        --remote-ip or -rip LISTEN_IP (ip address to forward [default : 127.0.0.1])
        --service or -sc SERVICE (Determine Service : [http])
   
        -h or --help                  (show this help message and exit)
