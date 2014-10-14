#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Joseph Herlant <herlantj@gmail.com>
# File name: hdfs_disk_usage_per_datanode.py
# Creation date: 2014-10-08
#
# Distributed under terms of the GNU GPLv3 license.

"""
This nagios active check parses the Hadoop HDFS web interface url:
http://<namenode>:<port>/dfsnodelist.jsp?whatNodes=LIVE
to check for active datanodes that use disk beyond the given thresholds.

The output includes performance datas and is truncated if longer than 1024
chars.

Tested on: Hadoop CDH3U5
"""

__author__ = 'Joseph Herlant'
__copyright__ = 'Copyright 2014, Joseph Herlant'
__credits__ = ['Joseph Herlant']
__license__ = 'GNU GPLv3'
__version__ = '1.0.2'
__maintainer__ = 'Joseph Herlant'
__email__ = 'herlantj@gmail.com'
__status__ = 'Production'
__website__ = 'https://github.com/aerostitch/'

from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import argparse, sys

if __name__ == '__main__':
    # use -h argument to get help
    parser = argparse.ArgumentParser(
        description='A Nagios check to verify all datanodes disk usage in \
                an HDFS cluster from the namenode web interface.')
    parser.add_argument('-n', '--namenode', required=True,
                        help='hostname of the namenode of the cluster')
    parser.add_argument('-p', '--port', type=int, default=50070,
                        help='port of the namenode http interface. \
                        Defaults to 50070.')
    parser.add_argument('-w', '--warning', type=int, default=80,
                        help='warning threshold. Defaults to 80.')
    parser.add_argument('-c', '--critical', type=int, default=90,
                        help='critical threshold. Defaults to 90.')
    args = parser.parse_args()

    # Get the web page from the namenode
    url = "http://%s:%d/dfsnodelist.jsp?whatNodes=LIVE" % \
            (args.namenode, args.port)
    try:
        page = Browser().open(url)
    except IOError:
        print 'CRITICAL: Cannot access namenode interface on %s:%d!' % \
                (args.namenode, args.port)
        sys.exit(2)

    # parse the page
    html = page.read()
    soup = BeautifulSoup(html)
    datanodes = soup.findAll('td', {'class' : 'name'})
    pcused = soup.findAll('td', {'class' : 'pcused', 'align' : 'right'})
    w_msg = ''
    c_msg = ''
    perfdata = ''
    for (idx, node) in enumerate(datanodes):
        pct = float(pcused[idx].contents[0].strip())
        node = datanodes[idx].findChildren('a')[0].contents[0].strip()
        if pct >= args.critical:
            c_msg += ' %s=%.1f%%,' % (node, pct)
            perfdata += ' %s=%.1f,' % (node, pct)
        elif pct >= args.warning:
            w_msg += ' %s=%.1f%%,' % (node, pct)
            perfdata += ' %s=%.1f,' % (node, pct)
        else:
            perfdata += ' %s=%.1f,' % (node, pct)

    # Prints the values and exits with the nagios exit code
    if len(c_msg) > 0:
        print ('CRITICAL:%s%s |%s' % (c_msg, w_msg, perfdata)).strip(',')[:1024]
        sys.exit(2)
    elif len(w_msg) > 0:
        print ('WARNING:%s |%s' % (w_msg, perfdata)).strip(',')[:1024]
        sys.exit(1)
    elif len(perfdata) == 0:
        print 'CRITICAL: Unable to find any node data in the page.'
        sys.exit(2)
    else:
        print ('OK |%s' % (perfdata)).strip(',')[:1024]
        sys.exit(0)

