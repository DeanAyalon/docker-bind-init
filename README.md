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

----
# Untesteed
- How would this behave for a file mount? (rather than mounting a directory)
