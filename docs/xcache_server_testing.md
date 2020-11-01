
# Testing 

## Pre-requisit

ATLAS doesn't make use of strong VO-based permissions at sites when placing data.

Many files on the grid at many sites are accessible via an anonymous user over https.

This could/should be changed but is beyond the scope of this tutorial.

You will need a valid grid proxy for a VO trusted by the back-end storage you're looking to access.

ECDF(Edinburgh) supports ATLAS,lhcb,dteam,gridpp and other VOs even if very few of these access/write data to this storage.


## Testing the Transparent XCache server directly

At Edinburgh we have 1 Transparent XCache in-front of 1 (DPM-based) SE.

 * gridpp09.ecdf.ed.ac.uk - XCache server
 * srm.glite.ecdf.ed.ac.uk -  SE head-node

To test the XCache server is working as expected in isolation we can try copying a file:

Test file: http://srm.glite.ecdf.ed.ac.uk/dpm/ecdf.ed.ac.uk/home/atlas/atlasdatadisk/rucio/data17_5TeV/05/2f/data17_5TeV.00340910.physics_Main.merge.AOD.f911_m1917._lb0264._0001.1
(may not be there when you try to run but as an example, feel free to try with any file you have access to)

### Direct copy (not via XCache)

To access this file directly from the head-node:

```
xrdcp root://srm.glite.ecdf.ed.ac.uk://dpm/ecdf.ed.ac.uk/home/atlas/atlasdatadisk/rucio/data17_5TeV/05/2f/data17_5TeV.00340910.physics_Main.merge.AOD.f911_m1917._lb0264._0001.1 .
```

When you run this the transfer should last for long enough for you to see the file being served from a disk node in Edinburgh named something like: `pool10.glite.ecdf.ed.ac.uk`


### Pseudo-3rd party copy (i.e. through an XCache)

I'm calling it pseudo-3rd party as there are 3 people involved. Please don't confuse this with TPC or 3rd party https work from other working-groups.

```
xrdcp xrootd://gridpp09.ecdf.ed.ac.uk://root://srm.glite.ecdf.ed.ac.uk://dpm/ecdf.ed.ac.uk/home/atlas/atlasdatadisk/rucio/data17_5TeV/05/2f/data17_5TeV.00340910.physics_Main.merge.AOD.f911_m1917._lb0264._0001.1 .
```

To verify that this is working as expected:

 * Did the file copy at all? if it did it must have gone through the proxy
 * Did your incoming transfer come from gridpp09.ecdf.ed.ac.uk? If so, great no funny business is going on and this is working as expected.


## Common Problems

### Permission denied 

 * Could this be caused by an incoming invalid credential (is your cert valid and does it have appropriate VOMS extensions?
 * Did you setup and run fetch-crl on the XCache server?
 * Do you have the correct VOMS/CA setup on the XCache server?

### Slow Cache Transfers

 * This can be caused by issues on the Cache server, but does the direct copy work with a higher rate when tested first?

### Anything Else?

You tell me




