#!/usr/bin/python

import socket
import Skype4Py

Port=12222

class Pipe:
    def __init__(self, skype, sock):
        self.skype = skype
        self.sock = sock
        self.buf = ""

    def run(self):
        while True:
            scmd = self.read()
            if not scmd:
                break
            cmd = self.skype.Command(scmd, Block=True)
            self.skype.SendCommand(cmd)
            self.sock.sendall((cmd.Reply + "\n").encode("utf-8"))

    def read(self):
        while True:
            d = self.sock.recv(1024)
            if not d:
                break
            self.buf += d
            n = self.buf.find("\n")
            if n >= 0:
                ret = self.buf[:n]
                self.buf = self.buf[n+1:]
                return ret
        return None

class Server:
    def __init__(self, skype, port):
        self.skype = skype
        self.port = port

    def start(self):
        server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_sock.bind(("", self.port))
        server_sock.listen(1)
        sock, addr = server_sock.accept()
        # TODO: use thread
        Pipe(self.skype, sock).run()


if __name__=="__main__":
    skype = Skype4Py.Skype()
    skype.Attach()
    server = Server(skype, Port)
    server.start()
