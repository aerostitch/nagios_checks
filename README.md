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

hdfs_datanode_balancing_status.py
---------------------------------

### Description

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

### Usage

```
usage: hdfs_datanode_balancing_status.py [-h] -n NAMENODE [-p PORT]
                                         [-w WARNING] [-c CRITICAL]

A Nagios check to verify that all datanodes of an HDFS cluster is in under the
balancing threshold using the namenode web interface.

optional arguments:
  -h, --help            show this help message and exit
  -n NAMENODE, --namenode NAMENODE
                        hostname of the namenode of the cluster
  -p PORT, --port PORT  port of the namenode http interface. Defaults to
                        50070.
  -w WARNING, --warning WARNING
                        warning threshold. If the datanode usage differs from
                        average usage to more than this threshold, raise a
                        warning. Defaults to 10.
  -c CRITICAL, --critical CRITICAL
                        critical threshold. If the datanode usage differs from
                        average usage to more than this threshold, raise a
                        critical. Defaults to 15.
```
