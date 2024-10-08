# Export Branch
This branch was created as an alternative implementation, using `docker create` and `docker export` to get the default mount path files

## The Plan
- [ ] Create template container with no mounts
- [ ] `docker export`
- [ ] Remove container
- [ ] Extract tar
- [ ] Copy into bind-mount

## Limits
Currently, I do not know how to check whether a bind mount is empty in the following case:
- Script is running within a Docker container, rather than on host
(AND)
- Image being initialized is minimal, without the `ls -A` command