#import clientConn
import docker
import logging
import random
import datetime
import re
import os


#client = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto')
#con = client.containers.list()[1]

def get_CPU_Percentage(con):
    conName = con.name
    cpupercentage = 0.00

    # Check if the container is running
    if (con.status != 'running'):
        raise ValueError('"%s" container is not running' % conName)

    # Get CPU Usage in percentage
    constat = con.stats(stream=False)
    prestats = constat['precpu_stats']
    cpustats = constat['cpu_stats']
    # print(cpustats)

    # cpuDelta = res.cpu_stats.cpu_usage.total_usage -  res.precpu_stats.cpu_usage.total_usage;
    # systemDelta = res.cpu_stats.system_cpu_usage - res.precpu_stats.system_cpu_usage;
    # var RESULT_CPU_USAGE = cpuDelta / systemDelta * 100;
    # CPUStats.CPUUsage.PercpuUsage

    prestats_totalusage = prestats['cpu_usage']['total_usage']
    stats_totalusage = cpustats['cpu_usage']['total_usage']
    numOfCPUCore = len(cpustats['cpu_usage']['percpu_usage'])
    logging.debug('prestats_totalusage: %s, stats_totalusage: %s, NoOfCore: %s' % (
    prestats_totalusage, stats_totalusage, numOfCPUCore))

    prestats_syscpu = float(prestats['system_cpu_usage'])
    stats_syscpu = float(cpustats['system_cpu_usage'])
    logging.debug('prestats_syscpu: %s, stats_syscpu: %s' % (prestats_syscpu, stats_syscpu))

    cpuDelta = float(stats_totalusage - prestats_totalusage)
    systemDelta = float(stats_syscpu - prestats_syscpu)

    if cpuDelta > 0 and systemDelta > 0:
        cpupercentage = (cpuDelta / systemDelta) * numOfCPUCore

    formattedcpupert = '{:.1%}'.format(cpupercentage)
    logging.debug('cpuDelta: %s, systemDelta: %s, cpu: %s' % (cpuDelta, systemDelta, cpupercentage))

    logging.info('"%s" Container CPU: %s ' % (conName, formattedcpupert))

    return (cpupercentage * 100)
