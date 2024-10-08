# Export Branch
This branch was created as an alternative implementation, using `docker create` and `docker export` to get the default mount path files

## The Plan
- [ ] Generate dynamic dockerfile based on container's empty bind mounts
  ```dockerfile
  FROM scratch
  COPY --from={IMAGE} {DEST} {DEST}
  ...
  CMD [""]
  ```
- [ ] Build without saving cache
- [ ] Create container 
- [ ] `docker export`
- [ ] Remove container and image
- [ ] Extract tar
- [ ] Copy into bind-mount

## Limits
Currently, I do not know how to check whether a bind mount is empty in the following case:
- Script is running within a Docker container, rather than on host
(AND)
- Image being initialized is minimal, without the `ls -A` command