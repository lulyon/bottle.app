# -*- coding: utf-8 -*-
"""
this serves as a 'loader' for some commonly basic use function
		usage: python <filename> [run|test|document] <host> <port>
"""

import gevent.monkey
gevent.monkey.patch_all()

from sys import argv
from subprocess import call
from datetime import datetime

# 注册libs及libs/vendor目录到importpath中
import libs.environment
current_time = lambda: str(datetime.now()).split(' ')[1].split('.')[0]

def run(host='127.0.0.1', port='8080'):
    """
    run       serves the application, accepts *args **kwargs
    """
    # usage: python . serve *args **kwargs
    print('=> %s : serving the application.'%current_time())

    from config.settings import settings
    from libs.app import Application
    application = Application(settings)

    application.run(server='gevent', host=str(host), port=int(port))

def test():
    """
    test        tests the application
    """
    # usage: python . test
    print('=> %s : testing the application.'%current_time())
    # calling nose's nosetests to test the application using the 'tests' module
    call(['nosetests', '-v', 'tests'])

def document():
    """
    document    documents the project
    """
    # usage: python . document
    print('=> %s : documenting in process.'%current_time())
    # calling pycco to document the this project
    directories = ['.', 'handlers', 'libs', 'models', 'setup', 'tests']
    call(['pycco', '-p'] + [directory + '/*.py' for directory in  directories])

# -----

# _the optional commands:_
options = [ 'run', 'test', 'document']
# evaling the command. if invalid command will print out a nicely formatted 'help' table
if len(argv) == 1 or argv[1] not in options:
    for option in options:
        print('  ->%s'%(eval(option).__doc__.split('\n')[1]))
else:
    if len(argv) >= 4:
        ip = argv[2]
        port = argv[3]
        eval(argv[1])(host=ip, port=port)
    else:
        eval(argv[1])()
