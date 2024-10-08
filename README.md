# What is this?
Small tool to initialize bind mounts with the image's default contents, just like Docker volumes.<br>
Bind mounts will only be initialized if they're empty, and the image has default contents for the mount path

## Purpose
No real purpose, one can always do these steps on their own, this served more for Python / Docker SDK practice

## Limits
Currently, this only works on containers made from images able to run `tail -f /dev/null` and `ls` - minimal images based on binaries will not work, and the script has yet to be designed to handle such a case.
- Alternatives are being tested, such as mounting a `sleep`/`tail` executable, but so far, not successfully

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
