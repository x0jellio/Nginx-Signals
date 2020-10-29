import time
import json
import signal
import os


def readConfiguration(signalNumber, frame):
    print ('(SIGHUP) reading configuration and restarting NGINX')
    os.system('brew services restart nginx')
    return

def terminateProcess(signalNumber, frame):
    print ('(SIGTERM) terminating the process')
    sys.exit()

filename = "/usr/local/var/log/nginx/access.log"

with open(filename, 'r') as f:
    while 1:
        where = f.tell()
        j = [ json.loads(lines) for lines in f.readlines() ]
        i = 0 
        if not j:
                time.sleep(1)
                f.seek(where)
        elif j:
            for i in range(0,len(j)):
                 if j[i]['status'] == '501':
                   readConfiguration(1,None) 
        else:
            print(j)


if __name__ == '__main__':

    signal.signal(signal.SIGTERM, terminateProcess)
    signal.signal(signal.SIGHUP, readConfiguration)

    # output current process id
    print('My PID is:', os.getpid())

    signal.pause()
