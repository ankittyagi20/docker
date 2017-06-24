#!/usr/bin/python
import os
import sys
sys.path.append('/var/dockerscale')
import docker
import getcpuperc
import time
import argparse

def get_args():
  try:
    parser = argparse.ArgumentParser(description='Pass the following required arguments for autoscaling the service running in docker')
    parser.add_argument('-u', metavar='--UPPER_THRESHOLD', type=int, required=True, help='Upper CPU threshold, after which service will be scaled')
    parser.add_argument('-l', metavar='--LOWER_THRESHOLD', type=int, required=True, help='Lower CPU threshold, after which service will be scaled down')
    parser.add_argument('-t', metavar='--COOLTIME', type=int, required=True, help='Time for which service containers will be monitored before scaling up or down. Before scaling down, the service will be monitored for half of this time')
    parser.add_argument('-i', metavar='--UPSCALEFACTOR', type=int, required=True, help='Service will be scaled up by the value set in this parameter')
    parser.add_argument('-b', metavar='--BASEPOOL', type=int, required=True, help='Minimum number of containers required for the service')
    parser.add_argument('-d', metavar='--DOWNSCALEFACTOR', type=int, required=True, help='Service will be scaled down by the value set in this parameter but not below base_pool, set with -b')
    parser.add_argument('-s', metavar='--SERVICES', nargs='+', type=str, required=True, help="List of services to be monitored, only the name of services. for e.g. -l ['service1', 'service2']")

    arguments = parser.parse_args()
    return arguments
  except Exception as e:
    print "Error: " + e.message

def scale_service(u_t, l_t, c_t, up_scale_factor, down_scale_factor, base_pool, scale_list):
  try:
    client = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto')
    cont_list = client.containers.list()

    #get the service list
    services = client.services.list()
    cpu = 0
    scale_up = False
    scale_down = False
    pool_count = 0

    #scale_list is the list of services passed as argument to the script that we want to run auto-scaling.
    #if service.name in scale_list:
    for service in services:
      if service.name in scale_list:
        current_pool = {}
        running_tasks = service.tasks(filters={'desired-state': 'running'})
        #pool_count = len(running_tasks)
        for task in running_tasks:
          container_id = task['Status']['ContainerStatus']['ContainerID']
          container_obj = client.containers.get(container_id=container_id)
          cpu = int(getcpuperc.get_CPU_Percentage(container_obj))
          end_time = time.time() + c_t 
          #c_t is the cool time for which cpu will be monitored consistently and scaling will be performed accordingly
          if cpu >= u_t:
            scale_up = True
            while (time.time() < end_time):
              cpu = int(getcpuperc.get_CPU_Percentage(container_obj))
              if cpu >= u_t:
                continue
              else:
                scale_up = False
                break

          if cpu <= l_t:
            scale_down = True
            while (time.time() < end_time/2):
              cpu = int(getcpuperc.get_CPU_Percentage(container_obj))
              if cpu <= l_t:
                coninue
              else:
                scale_down = False

          if scale_up == True:
            pool_count = len(running_tasks)
            print "Currently running tasks=%i.... Scaling up %s" %(pool_count, service.name)
            os.system("sudo docker service scale %s=%i" %(service.name, int(pool_count + up_scale_factor)))
          else:
            print service.name + " running with CPU below upper_threshold of " + str(u_t) + "%"

          if scale_down == True:
            pool_count = len(running_tasks)
            if pool_count > base_pool:
              print "Scaling down " + service.name 
              os.system("sudo docker service scale %s=%i" %(service.name, int(pool_count - down_scale_factor)))
          else:
            print service.name + " running with CPU above lower_threshold of " + str(l_t) + "%"
        running_tasks = service.tasks(filters={'desired-state': 'running'})
        pool_count = len(running_tasks)
        current_pool[service.name] = pool_count
    return current_pool

  except Exception as e:
    print "Something went wrong...exception: " + e.message
    sys.exit(2)

if __name__ == "__main__":
  print "Inside main"
  try:
    args = get_args()
    #print "Args: " + str(args)
    service_size = scale_service(u_t=args.u, l_t=args.l, c_t=args.t, up_scale_factor=args.i, down_scale_factor=args.d, base_pool=args.b, scale_list=args.s)
    print "Current pool size: " + str(service_size)
  except Exception as e:
    print "Error: " + e.message
