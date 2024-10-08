#!python3

from typing import cast

import os
import sys
import subprocess
from pathlib import Path

import docker
from docker.models.containers import Container

def files(mount, container = None): 
    if in_docker:
        # docker exec ls -A
        files = subprocess.check_output(['docker', 'exec', container, 
                                         'ls', '-A', mount['Destination']], 
                                        stderr=subprocess.DEVNULL)
        files = files.splitlines()
        # How do we handle minimal binary images? `ls` not recognized
            # Can't export the container and check its contents locally
            # VOLUMES ARE NOT PART OF THE CONTAINER
    else: files = os.listdir(mount['Source'])
    return len(files)

########################### SAND BOX ###########################

# in_docker = True
# print(files('.', 'suspicious_banach'))
# exit(2)

################################################################
##                      SCRIPT EXECUTION                      ##
################################################################

# Argument - Container to initialize empty bind mounts
if len(sys.argv) < 2: exit('Please specify a container for bind mount initialization')
container_name = sys.argv[1]

# Check if running in Docker
cgroup = Path('/proc/self/cgroup')
in_docker = Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text()

# Initialize Docker client
client = docker.from_env()

# Get container
try: container = cast(Container, client.containers.get(sys.argv[1]))
except: exit(f'Container "{container_name}" not found')

# Get container bind mounts
mounts = cast(list, container.attrs['Mounts'])
mounts = list(filter(lambda mount: mount['Type'] == 'bind', mounts))

# Check mount contents
empty_mounts = []
for mount in mounts:
    dest = mount['Destination']

    # Count files
    mount_files = files(mount, container_name)
    # Will fail if running as a Docker image trying to initialize minimal images

    if mount_files == 0:
        empty_mounts.append(mount)

print('empty', empty_mounts)