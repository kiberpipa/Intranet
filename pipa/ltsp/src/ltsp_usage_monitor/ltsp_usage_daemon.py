#!/usr/bin/python

import re
from datetime import datetime
import os
import sys
from glob import glob
import pwd
import socket
import logging
import daemon
import select
import stat

### Settings

LTSP_HOME = '/home/ltsp'
HOST=''
PORT=31000
DAEMON_CONF = '/home/hruske/projekti/pipa/kovchek/ltsp_usage_monitor/ltspstats.conf'
UNIX_SOCKET='/tmp/ltspstats'

M_AVG=6
M_THR=3

#### End Settings

# format: "Tue Nov 14 08:17:51 2006 uid: 1011 mousemoved: 0\n"
log_re = re.compile("^\w+\s(?P<month>\w+)\s(?P<day>\d+)\s(?P<hours>\d+)\W(?P<minutes>\d+)\W(?P<seconds>\d+)\s(?P<year>\d+)\suid\s(?P<uid>\d+)\s(mousemoved)\s(?P<mousemoved>\d)")
month = { 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12,}


def refresh():
    uname = pwd.getpwuid(int(m.groups()[7]))
    usage[uname.pw_name] = int(sum(term_list) > 3)

class TerminalStatsDaemon(daemon.Daemon):
    default_conf = DAEMON_CONF
    section = "ltspstats"
    socket = None
    
    def run(self):
        status = {}

        # bind tcp socket
        """
        try:
            ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssocket.bind((HOST,PORT))
            ssocket.listen(5) 
        except socket.error, (value,message):
            if ssocket:
                ssocket.close()
            logging.info("Could not open socket: " + message)
            sys.exit(1)
        """

        # cleanup unix socket
        if os.path.exists(UNIX_SOCKET):
            mode = os.stat(UNIX_SOCKET)[stat.ST_MODE]
            if stat.S_ISSOCK(mode):
                os.remove(UNIX_SOCKET)

        # bind unix socket
        try:
            usocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            usocket.bind(UNIX_SOCKET)
            usocket.listen(5)
        except socket.error, (value, message):
            if usocket:
                usocket.close()
            logging.info("Could not open local socket: " + message)
            sys.exit(1)

        os.chmod(UNIX_SOCKET, 666) # da lahko daemoni pisejo not.

        # main loop
        """
        input = [ssocket, usocket]
        """
        input = [usocket]
        output = []
        while 1:
            inputready,outputready,exceptready = select.select(input,output,[])
            for s in inputready:
                """
                # sprejemanje tcp povezav
                if s == ssocket:
                    client, address = ssocket.accept()
                    logging.info(address)
                    output.append(client)
                """
                # sprejemanje unix povezav
                elif s == usocket:
                    uclient, address = usocket.accept()
                    logging.info(address)
                    input.append(uclient)
                # pobiranje podatkov
                else:
                    data = s.recv(64)
                    m = log_re.match(data)
                    if m:
                        d = m.groupdict()
                        # tu se urejajo zbrane informacije
                        uname = pwd.getpwuid(int(d['uid']))
                        lst = status.get(uname.pw_name,[])
                        
                        lst.append((
                            datetime(int(d['year']),int(month[d['month']]), int(d['day']),int(d['hours']),int(d['minutes']),int(d['seconds'])),
                            int(d['mousemoved']),
                            ))
                        if len(lst) > M_AVG:
                            lst.pop(0)
                        
                        status[uname.pw_name] = lst

                    s.close()
                    input.remove(s)

            # posiljanje podatkov
            for s in outputready:
                
                s.send("
                
                """
                response = []
                all = []
                for user in status:
                    difference = datetime.now() - status[user][-1][0]
                    if difference.seconds < 32:
                        sum_to_be = []
                        for t in status[user]:
                            sum_to_be.append(t[1])
                        v = 1 <= int( sum(sum_to_be)/float(M_THR))
                        response.append('%s\t%d' % (user, int(v) ))
                        all.append(v)
                    else:
                        response.append('%s\t-' % (user,))
                response.extend( ['all\t%d' % sum(all), ''] )
                s.send("\n".join(response))
                s.close()
                output.remove(s)
                """



if __name__ == "__main__":
    if "nodaemon" in sys.argv:
        TerminalStatsDaemon().run()
    else:
        try:
            import psyco
            psyco.full()
        except ImportError:
            pass
        TerminalStatsDaemon().main()
