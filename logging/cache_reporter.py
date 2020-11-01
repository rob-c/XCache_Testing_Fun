#!/usr/bin/env python3.6

import os
import sys
from glob import glob
import struct
import time
import elasticsearch as es

ct = time.time()
start_time = ct - 3600
end_time = ct

site = 'Edinburgh'
collector = 'tatties.ph.ed.ac.uk'
collector_port = 9200
collector_auth = ('elastic','tek@Edinburgh;123')
reports = []
reports2 = {
        'sender': 'xCache',
        'site': site,
        'files': 0,
        'size': 0,
        'accesses': 0,
        'accesses_size': 0,
        'avg_lifetime': 0,
        'bytes_disk': 0,
        'bytes_ram': 0,
        'bytes_miss': 0,
        'time': ct * 1000
}


def get_info(filename):

    fin = open(filename, "rb")

    _, = struct.unpack('i', fin.read(4))
    # print ("file version:", _)
    bs, = struct.unpack('q', fin.read(8))
    # print ('bucket size:', bs)
    fs, = struct.unpack('q', fin.read(8))
    # print ('file size:', fs)

    buckets = int((fs - 1) / bs + 1)
    # print ('buckets:', buckets)

    StateVectorLengthInBytes = int((buckets - 1) / 8 + 1)
    sv = struct.unpack(str(StateVectorLengthInBytes) + 'B', fin.read(StateVectorLengthInBytes))  # disk written state vector
    # print ('disk written state vector:\n ->', sv, '<-')

    chksum, = struct.unpack('16s', fin.read(16))
    # print ('chksum:', chksum)

    time_of_creation, = struct.unpack('Q', fin.read(8))
    # print ('time of creation:', datetime.fromtimestamp(time_of_creation))

    rec = {
        'sender': 'xCache',
        'type': 'docs',
        'site': site,
        'file': filename.replace('/gridstorage/cache', '').replace('/atlas/rucio/', '').replace('.cinfo', ''),
        'size': fs,
        'created_at': time_of_creation * 1000
    }

    accesses, = struct.unpack('Q', fin.read(8))
    # print ('accesses:', accesses)

   
    reports2['size'] = reports2['size'] + fs
    reports2['accesses'] = reports2['accesses'] + accesses + 1
    reports2['accesses_size'] = reports2['accesses_size'] + (accesses + 1)*fs
    reports2['avg_lifetime'] = reports2['avg_lifetime'] + (ct - time_of_creation)

    min_access = max(0, accesses - 20)
    for a in range(min_access, accesses):
        attach_time, = struct.unpack('Q', fin.read(8))
        detach_time, = struct.unpack('Q', fin.read(8))
        bytes_disk, = struct.unpack('q', fin.read(8))
        bytes_ram, = struct.unpack('q', fin.read(8))
        bytes_missed, = struct.unpack('q', fin.read(8))
        if detach_time > start_time and detach_time < end_time:
            dp = rec.copy()
            dp['access'] = a
            dp['attached_at'] = attach_time * 1000
            dp['detached_at'] = detach_time * 1000
            dp['bytes_disk'] = bytes_disk
            dp['bytes_ram'] = bytes_ram
            dp['bytes_missed'] = bytes_missed
            reports.append(dp)

        reports2['bytes_disk'] = reports2['bytes_disk'] + bytes_disk
        reports2['bytes_ram'] = reports2['bytes_disk'] + bytes_ram
        reports2['bytes_miss'] = reports2['bytes_disk'] + bytes_missed
        

files = [y for x in os.walk('/cache') for y in glob(os.path.join(x[0], '*.cinfo'))]
# files += [y for x in os.walk('/cache') for y in glob(os.path.join(x[0], '*%'))]
for filename in files:
    #last_modification_time = os.stat(filename).st_mtime
    # print(filename, last_modification_time)
    #if last_modification_time > start_time and last_modification_time < end_time:
    get_info(filename)

es = es.Elasticsearch(hosts=[{'host': collector, 'port':collector_port}], http_auth=collector_auth)
print("xcache reporter - files touched:", len(reports))
if len(reports) > 0:
    for rep in reports:
        es.index(index="gridpp_xcache_sites", body=rep)
    print(reports)
else:
    print("xcache reporter - Nothing to report")
if len(files) != 0:
    reports2['files'] = len(files)
    reports2['avg_lifetime'] = reports2['avg_lifetime']/reports2['files']
    print(reports2)
    es.index(index="xcache_info", body=reports2)
