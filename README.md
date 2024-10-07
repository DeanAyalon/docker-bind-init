# Purpose
Small tool to initialize bind mounts with the image's default contents, just like Docker volumes.<br>
Bind mounts will only be initialized if they're empty, and the image has default contents for the mount path

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

----
# Untesteed
- How would this behave for a file mount? (rather tahn mounting a directory)