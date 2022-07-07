import socket
from threading import Thread
from typing import Callable, Any

try:
    import simplejson as json
except ImportError:
    import json
    
from easyplayer.utils.cs.client import User


class Server(object):
    def __init__(self, host: str = '127.0.0.1', port: int = 50000, debug: bool = False):
        """
        Easy Player CS server.
        
        :param host: Host.
        :param port: Port.
        :param debug: Whether to show messages.
        """
        self.sock = socket.socket()
        self.sock.bind((host, port))
        if debug:
            print(f'Bind {host}:{port}')
        self.users = []

        _empty_func = lambda user: None
        self._when_user = _empty_func
        self._debug = debug
        
    def run(self, requests: int = 10):
        """
        Start service and main loop.
        
        Use multithreading to process users.
        
        :param requests: Number of users listening.
        :return: None
        """
        self.sock.listen(requests)
        while True:
            sock, addr = self.sock.accept()
            if self._debug:
                print(f'Get connected: ({sock}, {addr})')
            user = User(sock, addr)
            self.users.append(user)
            t = Thread(target=self._when_user, args=(user, ))
            t.start()
            if self._debug:
                print('Started thread')
            
    def broadcast(self, data: Any):
        """
        Broadcast a message to all clients.
        
        :param data: Message data.
        :return: None
        """
        for user in self.users:
            user.send(json.dumps(data))
        if self._debug:
            print(f'Broadcast {data}')
            
    def when_user_connected(self, func: Callable[[User], Any]):
        """
        A decorator to decorate a callback function when user connect.
        
        Callback function must be like this:
        
        >>> import easyplayer as ep
        >>> server = ep.cs.Server()
        >>> @server.when_user_connected   # @server.when_user
        >>> def when_user_connected(user):   # Must have user argument
        >>>     ...

        :param func: Callback function.
        :return: None
        """
        self._when_user = func
        
    when_user = when_user_connected
