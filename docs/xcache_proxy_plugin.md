
# Transparent XCache

Transparent XCache is named as such because it's transparent/invisible to the end user/pilot/VO

This is achived though loading a plugin at runtime which modifies the client-side behaviour of XRootD tools/libraries.

This is fragile in the sense that a VO can easily turn this off or change this behaviour so it stops working, but to get work done at a site level without having to involve some 20 other experts this is the ideal step forward.

The plugin at present has a simple whitelist functionality which hasn't been tested with external access, but we can work on this.

## Compiling the plugin

### Pre-requisits

You will need a CentOS7 host perferably with CVMFS.

This isn't a strong requirement, but it makes life easier.

As for build dependencies, this has been tested with GCC-4.8 and CMake-2.8 as comes by default from the yum CentOS7 repos

### Build Instructions

The plugin used to achieve this is in the XrdCLROProxyPlugin folder of this repo.

To build it against XRootD v4.11.3:

```
cd XrdCLROProxyPlugin
mkdir build; cd build
cmake -DXROOTD_DIR=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/xrootd/4.11.3-x86_64-centos7/v4.11.3 ..
make -j
```

Congrats you should now have your plugin under: `XrdCLROProxyPlugin/build/src/libXrdClProxyRW-4.so`


This library can now be copied and used as expected.

