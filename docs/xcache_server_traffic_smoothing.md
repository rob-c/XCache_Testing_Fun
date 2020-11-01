
# Traffic Control CentOS7

Traffic control on CentOS7 is way better than it was on CentOS6. And is way better with kernel-ml/kernel-lt but that's up to you to deploy if you so choose.

If for some strange reason you don't have you will need to install the `iproute` package to  get access to the tools to use this functionality.

## Reasons to use this with XCache

 * If you have a single network connection this can help guarantee connections don't drop due to getting their rates pushed too low for fast connections.
 * If you have a fixed total bandwidth (up+down) higher up-stream this can help guarantee a minimum performance for a single connection

## How to Set this up

1) Add the FairQueue scheduler to your 
```
tc qdisc add dev p2p1 root fq
```

2) Now set a limit for how fast a single transfer can run through the XCache server. In this example all individual transfers and connections can only have 1G transfer speeds:
```
tc qdisc change dev p2p1 root fq maxrate 1gbit
```


## Testing this

To test this set an appropriately low rate such as 250M and limit transfers. Now when you transfer a pre-loaded file through your XCache you should see the speed limited to this rate as the maximum.

