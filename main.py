#!python3

from typing import cast

import os
import sys
import subprocess
from pathlib import Path

import docker
from docker.models.containers import Container

import shutil

def count_files(mount, container = None): 
    if in_docker:
        # docker exec ls -A
        try: files = subprocess.check_output(['docker', 'exec', container, 
                                         'ls', '-A', mount['Destination']], 
                                        stderr=subprocess.DEVNULL)
        except: 
            print('Cannot check minimal container files from within another container')
            exit('Run this Python script from your host machine to initialize the container')
        files = files.splitlines()
        # How do we handle minimal binary images? `ls` not recognized
            # Can't export the container and check its contents locally
            # VOLUMES ARE NOT PART OF THE CONTAINER
    else: files = os.listdir(mount['Source'])
    return len(files)

def dockcp(src, dest): 
    print('cp', src, dest)
    subprocess.check_output(['docker', 'cp', src, dest])

########################### SAND BOX ###########################


################################################################
##                      SCRIPT EXECUTION                      ##
################################################################

# Argument - Container to initialize empty bind mounts
if len(sys.argv) < 2: exit('Please specify a container for bind mount initialization')
container_name = sys.argv[1]

# Execution context
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    # Count files
    files = count_files(mount, container_name)
    # Will fail if running as a Docker image trying to initialize minimal images
    if files == 0: empty_mounts.append(mount)

if not len(empty_mounts): exit('No empty bind mounts to initialize')

# Create template container from image
img = container.attrs['Config']['Image']
temp_container = cast(Container, client.containers.create(img, ['']))

# Export container data
subprocess.check_output(['docker', 'export', '-o', f'exports/{img}.tar', 
                         temp_container.name])
shutil.unpack_archive(f'exports/{img}.tar', extract_dir=f'exports/{img}')

# Remove container and archive
os.remove(f'exports/{img}.tar')
temp_container.remove()

# Initialize bind mounts - works even if the container is not running!
for mount in empty_mounts:
    dest = mount['Destination']
    src = f'exports/{img}{dest}'
    fulldest = f'{container_name}:{dest}'
    try: files = os.listdir(src)
    except: files = []

    if len(files): 
        print('Initializing ' + fulldest)
        dockcp(src + '/.', fulldest)
    else: print(fulldest + ' empty by default')

# Remove extract
shutil.rmtree(f'exports/{img}')