# Use
This tool can either be used as a Python script - Requires [Poetry](https://python-poetry.org/)
```sh
poetry install                      # Install dependencies using Poetry
python3 ./main.py [containername]   # Initialize empty bind mounts for 'containername'
```

It can also be used as a standalone Docker container:
```sh
docker compose run --rm init [containername]
```

To use it without the compose file:
```sh
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock deanayalon/bind-init [containername]
```

# Limits
- Unable to check binary containers' mount data When running as a Docker container
  > To initialize minimal containers, run the Python script from the host machine
- Launching another container can be resource-expensive and may not always work. 
- Some processes do not respond to real-time file changes and may need to be restarted anyway
- Deleting a bind mount from host while a container is running will cause the script to fail if running from a container, and to skip the mount if running from host
- Does not initialize file mounts or named volumes
  > Perhaps possible to initialize file mounts when they do not yet exist

----
# Need Testing
- Check behavior when binding a directory to a file
  > Host mount diretory created, image default contains file<br>
  > `listdir` should fail when trying to initialize mount