
# Using a Transparent Proxy Plugin


## Defining the environment

The Transparent XCache makes use of a whitelist of XRootD URLs to re-write (`XROOT_PROXY_INCL_DOMAINS`).
When a file is opened the URL to the file is re-written to go via a proxy  (`XROOT_PROXY`).

This is achieved by XROOT always loading a plugin from the client side when a file-access is requested (`XRD_PLUGIN`).


```
# XCache server
export XROOT_PROXY="xroot://gridpp09.ecdf.ed.ac.uk:1094//"
# SE HeadNode
export XROOT_PROXY_INCL_DOMAINS="srm.glite.ecdf.ed.ac.uk"
# TXP proxy-plugin location
export XRD_PLUGIN=/root/libXrdClProxyRW-4.so
```

## Testing the Transparent Proxy

In order to test the Transparent XCache Plugin you have just built you will need to define the environmental vairables as above.

You will want to adapt these to your use-case.

### Testing with the XCache you built the plugin for

If you built your plugin for XRootD 4.11.3 you will need to use something like the following to make sure the plugin is loaded at runtime correctly.

```
LD_LIBRARY_PATH=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/xrootd/4.11.3-x86_64-centos7/v4.11.3/lib /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/xrootd/4.11.3-x86_64-centos7/v4.11.3/bin/xrdcp root://srm.glite.ecdf.ed.ac.uk://dpm/ecdf.ed.ac.uk/home/atlas/atlasdatadisk/rucio/data17_5TeV/05/2f/data17_5TeV.00340910.physics_Main.merge.AOD.f911_m1917._lb0264._0001.1 .
```

This should copy the same example file from the XCache server, not from the storage directly. The transparent component of the setup (the TXP) has told XRootD to use the XCache proxy 

### Testing with a different XCache release

XRootD allows for compatible plugins between releases to be loaded. This means that if the above testing worked for you the following will as well.

```
LD_LIBRARY_PATH=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/xrootd/4.12.4-x86_64-centos7/v4.12.4/lib /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/xrootd/4.12.4-x86_64-centos7/v4.12.4/bin/xrdcp root://srm.glite.ecdf.ed.ac.uk://dpm/ecdf.ed.ac.uk/home/atlas/atlasdatadisk/rucio/data17_5TeV/05/2f/data17_5TeV.00340910.physics_Main.merge.AOD.f911_m1917._lb0264._0001.1 .
```

NB:

This only works for compatible releaes of XRootD and 3rd-party plugins. i.e. XRootD 4.x plugins are not compatible with XRootD 5.x installs


### Common problems

* If your URL wasn't modified was the Plugin loaded?
* If your Plugin causes a segfault or worse when loading was it compiled for the same arch (64bit-CentOS7-XRootD-4.x)?
* Are you using the same major version of XCache?

