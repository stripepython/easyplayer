"""
Easy Player install requirements tool module.
"""

from subprocess import Popen


def install_requirements():
    """
    Install all requirements Easy Player need.
    
    :return: None
    """
    requirements = '''simplejson==3.17.2,pypiwin32'''.split(',')
    for r in requirements:
        Popen(r)
