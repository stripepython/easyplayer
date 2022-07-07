from typing import Union, Any
import socket

try:
    import simplejson as json
except ImportError:
    import json
    
    
class User(object):
    def __init__(self, sock: socket.socket, address: Any):
        """
        Create a user object.
        
        :param sock: socket.socket object.
        :param address: The address of this user.
        """
        self.sock = sock
        self.addr = address
        
    def send(self, data: Union[list, dict]):
        """
        Send data to this user.
        
        :param data: Data content.
        :return: None
        """
        string = json.dumps(data)
        self.sock.send(string.encode('utf-8'))
        
    def close(self):
        """
        Force existing links to close.
        
        :return: None
        """
        self.sock.close()
        
    def get(self, byte: int = 65536):
        """
        Get data of this user.
        
        :param byte: Maximum bytes to read.
        :return: Data.
        """
        return json.loads(self.sock.recv(byte).decode('utf-8'))
        

class Client(object):
    def __init__(self, host: str = '127.0.0.1', port: int = 50000):
        """
        Easy Player CS client.
        
        :param host: Server host.
        :param port: Server port.
        """
        self.sock = socket.socket()
        self.sock.connect((host, port))
        
    def send(self, data: Union[list, dict]):
        """
        Send data to server.

        :param data: Data content.
        :return: None
        """
        string = json.dumps(data)
        self.sock.send(string.encode('utf-8'))
        
    def get(self, byte: int = 65536):
        """
        Get data of this user.

        :param byte: Maximum bytes to read.
        :return: Data.
        """
        return json.loads(self.sock.recv(byte).decode('utf-8'))
    
    def close(self):
        """
        Force existing links to close.

        :return: None
        """
        self.sock.close()
