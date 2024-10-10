# What is this?
Small tool to initialize bind mounts with the image's default contents, just like Docker volumes.<br>
Bind mounts will only be initialized if they're empty, and the image has default contents for the mount path

[![Source](https://img.shields.io/badge/Source-121011?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DeanAyalon/docker-bind-init)

## Table of Contents
<!-- TOC -->

- [What is this?](#what-is-this)
    - [Table of Contents](#table-of-contents)
- [Use](#use)
- [Limits](#limits)
    - [Running within Docker](#running-within-docker)
- [Info](#info)
    - [Purpose](#purpose)
    - [Featured Technologies](#featured-technologies)

<!-- /TOC -->

# Use
This tool can either be used as a Python script - Requires [Poetry](https://python-poetry.org/)
```sh
python3 -m venv .venv
poetry install
python3 ./main.py [containername]
```

It can also be used as a standalone Docker container, but has [limited functionality](#running-within-docker)
```sh
docker compose run --rm init [containername]
```

To use it without the compose file:
```sh
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock deanayalon/bind-init [containername]
```

# Limits
- Launching another container can be resource-expensive
- Some processes do not respond to real-time file changes and may need to be restarted anyway
- Deleting a bind mount from host while a container is running will cause the script to fail if running from a container, and to skip the mount if running from host
- Does not initialize file mounts or named volumes
  > Perhaps possible to initialize file mounts when they do not yet exist

## Running within Docker
These limits **only apply when running the script within its Docker image**, rather than on the host machine
- Unable to check minimal containers' mount data - **Cannot initialize minimal containers**
  > Uses `docker exec ls` to check mount contents, ls not recognized in minimal images (based on scratch)
- Cannot initialize stopped images (Can't perform `docker exec`)

# Info
## Purpose
No real purpose, one can always do these steps manually with ease.<br>
This served more to learn Python/Docker concepts, and to practice the Docker SDK

## Featured Technologies
[![Docker](https://img.shields.io/badge/docker-1D63ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/deanayalon/bind-init)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Poetry](https://img.shields.io/badge/poetry-1d293a?style=for-the-badge&logo=poetry&logoColor=#60A5FA)
