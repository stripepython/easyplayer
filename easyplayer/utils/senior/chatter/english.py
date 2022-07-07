import sys
import os
import aiml

__all__ = ['Chatter']
    
    
class Chatter(object):
    def __init__(self, cls: bool = False):
        path = getattr(sys.modules['aiml'], '__file__', None)
        self._path = os.path.dirname(os.path.abspath(path))
        
        self._alice_path = os.path.join(self._path, 'botdata', 'alice')
        cwd = os.getcwd()
        
        os.chdir(self._alice_path)
        self._robot = aiml.Kernel()
        self._robot.learn('startup.xml')
        self._robot.respond('LOAD ALICE')
        
        os.chdir(cwd)
        if cls:
            os.system('cls')
        
    def chat(self, message: str):
        return self._robot.respond(message)
