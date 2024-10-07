#!python3
from pathlib import Path
from typing import cast

import sys
import os
import subprocess

import docker
from docker.models.containers import Container

################################################################
##                      SCRIPT EXECUTION                      ##
################################################################

# Argument - Container to initialize empty bind mounts
if len(sys.argv) < 2: exit('Please specify a container for bind mount intiialization')
container_name = sys.argv[1]

# Initialize Docker client
client = docker.from_env()

# Check if running inside a Docker container
cgroup = Path('/proc/self/cgroup')
in_docker = Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text()

# Get container
try: container = cast(Container, client.containers.get(sys.argv[1]))
except: exit(f'Container "{container_name}" not found')

# Get container bind mounts
mounts = cast(list, container.attrs['Mounts'])
mounts = list(filter(lambda mount: mount['Type'] == 'bind', mounts))

# Create template container from image
image = container.attrs['Image']
img_template = client.containers.run(image, 'tail -f /dev/null', detach = True, remove = True)

# DOCKER CP DOES NOT SUPPORT CONTAINER -> CONTAINER COPY!
#     print(f'docker cp {img_template.name}:{mount['Destination']} to {container.name}')
#     try: subprocess.check_output(['docker', 'cp', 
#                             img_template.name + ':' + mount['Destination'], 
#                             container.name + ':' + mount['Destination']])
#     except: print(mount['Destination'] + ' does not exist by default on the ' + image + ' image')
    
def cp(src, dest):
    subprocess.check_output(['docker', 'cp', src, dest])

# Check if running inside a container

# Populate empty bind mounts
for mount in mounts:
    # CHECK IF MOUNT IS EMPTY
    if in_docker:
        try: 
            cp(img_template.name + ':' + mount['Destination'], '/tmp/mnt')
            cp('/tmp/mnt/.', container.name + ":" + mount['Destination'])
            subprocess.check_output(['rm', '-rf', '/tmp/mnt'])
        except: print(f'{mount['Destination']} does not exist by default on the {image} image')

    else: 
        try: cp(img_template.name + ':' + mount['Destination'] + '/.', mount['Source'])
        except: print(f'{mount['Destination']} does not exist by default on the {image} image')