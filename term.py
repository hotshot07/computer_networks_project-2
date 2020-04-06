# Python script to open 3 new terminals on a mac

# Subprocess module isn't working as I'd like it to

import os


for i in range(2):
    os.system('open -a Terminal .')

# from subprocess import Popen, PIPE


# def subprocess_cmd(dr, cmd1, cmd2):
#     p1 = Popen(cmd1.split(), stdout=PIPE, cwd=dr)
#     p2 = Popen(cmd2.split(), stdin=p1.stdout, stdout=PIPE, cwd=dr)
#     p1.stdout.close()
#     return p2.communicate()[0]


# subprocess_cmd('/Users/hotshot07/Desktop/chatroom',
#                    'open -a Terminal', 'python3 server.py')
