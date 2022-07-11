"""
Easy Player English chatter module.
"""

import sys
import os
import aiml

from easyplayer.exceptions import EasyPlayerChatterError

__all__ = ['Chatter']
    
    
class Chatter(object):
    def __init__(self):
        """
        Easy Player English chatter. By AIML.
        """
        path = getattr(sys.modules['aiml'], '__file__', None)
        self._path = os.path.dirname(os.path.abspath(path))
        
        self._alice_path = os.path.join(self._path, 'botdata', 'alice')
        cwd = os.getcwd()
        
        os.chdir(self._alice_path)
        try:
            self._robot = aiml.Kernel()
            self._robot.learn('startup.xml')
            self._robot.respond('LOAD ALICE')
        except AttributeError:
            raise EasyPlayerChatterError(
                '\nIf you want to use it, please change module aiml/Kernel.py line 201\n'
                'start = time.clock()\n'
                'to\n'
                'start = time.time()\n'
                'And change line 204\n'
                'print( "done (%.2f seconds)" % (time.clock() - start) )\n'
                'to\n'
                'print("done (%.2f seconds)" % (time.time() - start))'
            )
        
        os.chdir(cwd)
        
    def chat(self, message: str):
        """
        Enter the chat information in English and return the chat reply content.

        :param message: The chat information in English.
        :return: The chat reply content.
        """
        return self._robot.respond(message)
