
# Setting Up an XCache server for GridPP

## Old instructions for setting up an XCache

[Here be Old Instructions](xcache_server_setup_old.md)

## Setting up the XCache via SystemD

### Setup the host to support XRootD with grid X509 authentication

This involves setting up:

 * Valid hostcert
 * VOMS packages for supported VOs
 * CA for trusted CAs
 * `fetch-crl` to update CRLs

You will need the xrootd packages from epel.
You should install tcmalloc as well from gperftools-devel gperftools-libs.

### XRootD config

To have SystemD integration with the XCache service you will need to use a config file named similar to `/etc/xrootd/xrootd-XXX.cfg`.

The example below is from a new XCache server which has been launched at ECDF:
 * Cached Data located at: `/gridstorage/cache/`
 * Create a secure token for this instance: `sec.protocol sss -s /etc/grid-security/xrd/sss.keytab.grp -c /etc/grid-security/xrd/sss.keytab.grp`
 * Copy the host certificate
 * Change ownership: `chown -R xrootd:xrootd /gridstorage/cache/`
 * Change ownership: `chown -R xrootd:xrootd /etc/grid-security/xrd`
 * Change ownership: `chown -R xrootd:xrootd /etc/grid-security/xrootd`


`/etc/xrootd/xrootd-gridppXCache.cfg`:
```
xrootd.trace debug
ofs.trace debug
xrd.trace debug
cms.trace debug
sec.trace debug

ofs.osslib    libXrdPss.so
pss.cachelib  libXrdFileCache.so
pfc.ram       1G
pfc.diskusage 0.5 0.8
pfc.blocksize 1M
pfc.prefetch  0
oss.localroot /gridstorage/cache/

all.export /xroot:/
all.export /root:/
pss.origin =
pss.setopt DebugLevel 3
pss.setopt ParStreamsPerPhyConn 4

# Allow all WN
xrd.allow host *.ecdf.ed.ac.uk

#xrootd.seclib libXrdSec.so
sec.protocol /usr/lib64 gsi -crl:3 -key:/etc/grid-security/xrootd/hostkey.pem -cert:/etc/grid-security/xrootd/hostcert.pem -md:sha256:sha1 -ca:2 -gmapopt:10 -vomsfun:/usr/lib64/libXrdSecgsiVOMS-4.so

# Use SSS for authentication
sec.protocol sss -s /etc/grid-security/xrd/sss.keytab.grp -c /etc/grid-security/xrd/sss.keytab.grp
# Use SSS for storage which are only servers under glite.ecdf.ed.ac.uk
sec.protbind *glite.ecdf.ed.ac.uk only sss

if exec cmsd

xrd.port 3121

else

xrd.port 1094

fi
```

### SystemD Service config for XRootD@gridppXCache

XRootD has a very nice integration with SystemD. Users of DPM will be familiar with this.

We will create the config file above and this gives us a service named: `xrootd@gridppXCache`

There are some useful optimisations in this file, including the `ExecStartPre` lines which are required to fix the lock file location being in a volatile directory which gets cleared on reboots.

`mkdir -p /etc/systemd/system/xrootd@gridppXCache.service.d`

`/etc/systemd/system/xrootd@gridppXCache.service.d/override.conf`:
```
[Service]
Restart=always
RestartSec=3

PermissionsStartOnly=true
ExecStartPre=-/usr/bin/mkdir -p /var/run/xrootd
ExecStartPre=/usr/bin/chown -R xrootd:xrootd /var/run/xrootd/
RuntimeDirectory=xrootd

Environment=LD_PRELOAD=/usr/lib64/libtcmalloc.so
# rcurrie increasing debug for debugging issues
Environment=XrdSecDEBUG=5
# rcurrie following: https://github.com/wyang007/rucioN2N-for-Xcache/wiki/Introduction-to-Xrootd-N2N-for-Disk-Caching-Proxy-(Xcache)-utilizing-RUCIO-metalink
Environment=TCMALLOC_RELEASE_RATE=10
# Enable Local file metalink processing
Environment=XRD_METALINKPROCESSING=1
# Enable Local file metalink processing
Environment=XRD_LOCALMETALINKFILE=1
# Turn off wait on error before retry
Environment=XRD_STREAMERRORWINDOW=5
# Increase number of retries before giving up
Environment=XRD_CONNECTIONRETRY=50
# Increase timeout on streaming
Environment=XRD_STREAMTIMEOUT=120
# Enable TCPKEEPALIVE
Environment=XRD_TCPKEEPALIVE=1
# Bump up number of workers
Environment=XRD_WORKERTHREADS=12
# Keep to V4 mode
Environment=XRD_NETWORKSTACK=IPv4
# Incease loglevel
Environment=XRD_LOGLEVEL=Debug
```

### Enabling service

To enable and start the service with systemd: `systemctl enable --now xrootd@gridppXCache`


# CmsD Service

If you so chose you can also setup the same for `cmsd`. For this I would still recommend  the above overrides as use the service name `cmsd@gridppXCache`

### Firewall

Add an appropriate firewall rule into your iptables and ip6tables to allow external servers to access your XCache.

```
-A INPUT -p tcp -m tcp --dport 1094 -j ACCEPT -m comment --comment "allow xrootd"
```


