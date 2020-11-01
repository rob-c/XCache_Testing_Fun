
# How to monitor XCache

## What is needed from XCache monitoring


## Let someone else do it

Get in touch with ECDF to get the latest monitoring config which will support the latest and greatest.


## I want to do it myself

The simplest way to monitor the XCache usage is to rely on XCache's internal metrics. This information can be fed into an elastic-search cluster for monitoring/analysis after the fact.

This is meta-data stored alongside files in the cache in `.cinfo` files. These contain data in the read/written amount of data per-file.

If you plan to use this yourself take care to change the site name and elastic-search credentials based on your use-case.

