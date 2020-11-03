
# How to monitor XCache

## What is needed from XCache monitoring


* Ingress/Egress statistics
* Successful/Broken/Bad/Cancelled Transfer statistics
* Impact of Network Rate Limiting
* Read size statistics


## Let someone else do it

Get in touch with ECDF to get the latest monitoring config which will support the latest and greatest.


## I want to do it myself

### Monitoring Data usage

The simplest way to monitor the XCache data usage is to rely on XCache's internal metrics. This information can be fed into an elastic-search cluster for monitoring/analysis after the fact.

This is meta-data stored alongside files in the cache in `.cinfo` files. These contain data in the read/written amount of data per-file.

```
#Run once per hour
python ./logging/cache_reporter.py
```

If you plan to use this yourself take care to change the site name and elastic-search credentials based on your use-case.

This example is designed to run once per-hour as it performs a walk through the cached data structure. Future improvements may mean this can run closer to real-time but as of now this is WIP.


### Monitoring the Service state

To Monitor the state of the current XCache service you need to monitor the logs directly.

An example on how to parse these is in the logging directory of this repo. 

```
logstash  ./logging/logstash.conf
```

### Monitor the Service for system stress/use

This can be achieved through either monitoring your service with a solution such as node_exporter or using metricbeat if you want to combine all of your metrics into the one elastic-search solution.


