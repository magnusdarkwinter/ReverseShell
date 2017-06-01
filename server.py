#!/usr/bin/env python3

import sys
import socket
import threading
import paramiko

KEYNAME = "rsa.key"
HOST = "127.0.0.1"
PORT = 8080
USERNAME = "root"
PASSWORD = "toor"
HOSTKEY = paramiko.RSAKey(filename=KEYNAME)

class Server(paramiko.ServerInterface):
    '''Paramiko server to connect via ssh'''
    def __init__(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == USERNAME) and (password == PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def main():
    '''Entry point if called as an exeutable'''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(100)
        print("[+] Listening for connection...")
        client, addr = sock.accept()
    except Exception as exc:
        print("[-] Listen/bind/accept failed: \n" + str(exc))
        sys.exit(1)
    print("[+] Connection to {0} established on port {1}".format(addr[0], addr[1]))

    try:
        transport = paramiko.Transport(client)
        try:
            transport.load_server_moduli()
        except:
            print("[-] Failed to load moduli: gex will be unsupported.")
            raise
        transport.add_server_key(HOSTKEY)
        server = Server()
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            print("[-] SSH negotiation failed.")
        chan = transport.accept(20)
        print("[+] Authenticated!")
        print(chan.recv(1024))
        while True:
            command = str(input(">>>").strip('\n')).encode()
            chan.send(command)
            print(str(chan.recv(1024)) + str('\n'))
    except Exception as exc:
        print("[-] Caught exception: \n" + str(exc))
        try:
            transport.close()
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()