Nagios checks repository
========================

Here you'll find some of the nagios checks I made and leave available for
everyone to use.

hdfs_disk_usage_per_datanode.py
-------------------------------

### Description

This nagios active check parses the Hadoop HDFS web interface url:
http://<namenode>:<port>/dfsnodelist.jsp?whatNodes=LIVE
to check for active datanodes that use disk beyond the given thresholds.

The output includes performance datas and is truncated if longer than 1024
chars.

Tested on: Hadoop CDH3U5

### Usage

```
usage: hdfs_disk_usage_per_datanode.py [-h] -n NAMENODE [-p PORT] [-w WARNING]
                                       [-c CRITICAL]

A Nagios check to verify all datanodes of an HDFS cluster from the namenode
web interface.

optional arguments:
  -h, --help            show this help message and exit
  -n NAMENODE, --namenode NAMENODE
                        hostname of the namenode of the cluster
  -p PORT, --port PORT  port of the namenode http interface. Defaults to
                        50070.
  -w WARNING, --warning WARNING
                        warning threshold. Defaults to 80.
  -c CRITICAL, --critical CRITICAL
                        critical threshold. Defaults to 90.
```
