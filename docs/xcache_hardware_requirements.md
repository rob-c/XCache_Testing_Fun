
# Hardware requirements

## Disk

### Transparent XCache

For testing at ECDF we have a pool of 1TB Disks which provides ~10TB of cache space for ZFS
This server makes use of 24GB of RAM for ZFS caching.

You will need to mount the storage you intend to use for caching as a POSIX filesystem. It is unknown if any non-POSIX filesystem can be successfully used for this.

If you're able to configure your block size (or recordsize in ZFS) make sure the number matches: `pfc.blocksize 1M` in your xcache config for best performance.

### Opaque XCache

The first Opaque XCache. An XCache which was setup with the VOs direct involvement. Was setup at Birmingham with the ATLAS VO.

The Storage configuration for this is:

TODO

## Network

### Transparent XCache

At ECDF the storage servers and the XCache server are both behind a 10G switch.
The compute at the site is behind a separate 10G switch and is not managed by the Tier2 admin.


### Opaque XCache

At Birmingham the XCache server is attached to the storage at Manchester.

This server has a XXG connection and is pulls data from Manchester which has a YYG external connection to JANET.

TODO

