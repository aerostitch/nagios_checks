#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Joseph Herlant <herlantj@gmail.com>
# File name: hdfs_datanode_balancing_status.py
# Creation date: 2014-10-08
#
# Distributed under terms of the GNU GPLv3 license.

"""
This nagios active check parses the Hadoop HDFS web interface url:
http://<namenode>:<port>/dfsnodelist.jsp?whatNodes=LIVE
to check that no datanode is beyond the balancing threshold (in both ways).
The goal of this check is to check if the balancer needs to be run manually and
do its job correctly (while running for example in cron jobs).

The output includes performance datas and is truncated if longer than 1024
chars. The values of the output are the variation between the average disk
usage of the nodes over the cluster and the disk usage of the current node on
the cluster.
A negative value of X means that the node is X percent under the average disk
usage of the datanodes over the cluster. A positive value means that it's over
the average.

Tested on: Hadoop CDH3U5
"""

__author__ = 'Joseph Herlant'
__copyright__ = 'Copyright 2014, Joseph Herlant'
__credits__ = ['Joseph Herlant']
__license__ = 'GNU GPLv3'
__version__ = '1.0.0'
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
        description='A Nagios check to verify that all datanodes of an HDFS \
                cluster is in under the balancing threshold \
                using the namenode web interface.')
    parser.add_argument('-n', '--namenode', required=True,
                        help='hostname of the namenode of the cluster')
    parser.add_argument('-p', '--port', type=int, default=50070,
                        help='port of the namenode http interface. \
                        Defaults to 50070.')
    parser.add_argument(
        '-w', '--warning', type=int, default=10,
        help='warning threshold. If the datanode usage differs from average \
        usage to more than this threshold, raise a warning. Defaults to 10.'
        )
    parser.add_argument(
        '-c', '--critical', type=int, default=15,
        help='critical threshold.  If the datanode usage differs from average \
        usage to more than this threshold, raise a critical. Defaults to 15.'
        )
    args = parser.parse_args()

    # Get the web page from the namenode
    url = "http://%s:%d/dfsnodelist.jsp?whatNodes=LIVE" % (args.namenode, args.port)
    try:
        page = Browser().open(url)
    except IOError:
        print 'CRITICAL: Cannot access namenode interface on %s:%d!' % (args.namenode, args.port)
        sys.exit(2)

    # parse the page and storing the {datanode: pct_usage} hash
    html = page.read()
    soup = BeautifulSoup(html)
    datanodes = soup.findAll('td', {'class' : 'name'})
    pcused = soup.findAll('td', {'class' : 'pcused', 'align' : 'right'})
    nodes_pct = {}
    for (idx, node) in enumerate(datanodes):
        pct = float(pcused[idx].contents[0].strip())
        node = datanodes[idx].findChildren('a')[0].contents[0].strip()
        nodes_pct[node] = pct

    # Each node variation against the average pct must be under the threshold
    w_msg = ''
    c_msg = ''
    perfdata = ''
    avg = 0
    if len(nodes_pct) > 0:
        avg = float(sum(nodes_pct.values()))/len(nodes_pct)
    else:
        print 'CRITICAL: Unable to find any node.'
        sys.exit(2)

    for (node, pct) in nodes_pct.items():
        if abs(pct-avg) >= args.critical:
            c_msg += ' %s=%.1f,' % (node, pct-avg)
            perfdata += ' %s=%.1f,' % (node, pct-avg)
        elif abs(avg-pct) >= args.warning:
            w_msg += ' %s=%.1f,' % (node, pct-avg)
            perfdata += ' %s=%.1f,' % (node, pct-avg)
        else:
            perfdata += ' %s=%.1f,' % (node, pct-avg)

    # Prints the values and exits with the nagios exit code
    if len(c_msg) > 0:
        print ('CRITICAL:%s%s |%s' % (c_msg, w_msg, perfdata)).strip(',')[:1024]
        sys.exit(2)
    elif len(w_msg) > 0:
        print ('WARNING:%s |%s' % (w_msg, perfdata)).strip(',')[:1024]
        sys.exit(1)
    else:
        print ('OK |%s' % (perfdata)).strip(',')[:1024]
        sys.exit(0)

