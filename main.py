#!python3
from typing import cast

import sys
import subprocess
from pathlib import Path

import docker
from docker.models.containers import Container

# TODO implement with Docker SDK?
def cp(src, dest): subprocess.check_output(['docker', 'cp', src, dest])

# TODO implement with Docker SDK?
def files(container, src): 
    try: files = subprocess.check_output(['docker', 'exec', container, 'ls', '-A', src], 
                                         stderr=subprocess.DEVNULL)
    except: files = ''
    return len(files.splitlines())

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
img_name = container.attrs['Config']['Image']
img_template = client.containers.run(image, 'tail -f /dev/null', detach = True, remove = True)

# DOCKER CP DOES NOT SUPPORT CONTAINER -> CONTAINER COPY!
#     print(f'docker cp {img_template.name}:{mount['Destination']} to {container.name}')
#     try: subprocess.check_output(['docker', 'cp', 
#                             img_template.name + ':' + mount['Destination'], 
#                             container.name + ':' + mount['Destination']])
#     except: print(mount['Destination'] + ' does not exist by default on the ' + image + ' image')

# Check if running inside a container

# Populate empty bind mounts
for mount in mounts:
    dest = mount['Destination']
    # Check if mount is empty
    container_files = files(container.name, dest)
    img_files = files(img_template.name, dest)

    if not img_files:
        print(f'{dest} does not exist by default on the {img_name} image')
    elif container_files:
        print(dest + ' already initialized, skipping')
    else: 
        # Copying between containers is not supported!
        print(f'Initializing {dest} with the default contents from {img_name}')

        if in_docker:
            # Copy to /tmp/mnt, then to the container
            cp(img_template.name + ':' + dest, '/tmp/mnt')
            cp('/tmp/mnt/.', container.name + ":" + dest)
            # TODO implement with native Python
            subprocess.check_output(['rm', '-rf', '/tmp/mnt'])

        else: # Copy to host mount path
            cp(img_template.name + ':' + dest + '/.', mount['Source'])

img_template.remove(force = True)