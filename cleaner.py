__author__ = 'yury'
import datetime
import argparse
import httplib
import json
import re

# python elastic_clean.py --host search-xxx.eu-west-1.es.amazonaws.com  --days 30

parser = argparse.ArgumentParser(description='Clean Elastic Cluster')
parser.add_argument("--host", required=True)
parser.add_argument("--days", required=True, type=int)
c = parser.parse_args()

conn = httplib.HTTPConnection(c.host)
conn.request("GET", "/_cat/indices?h=index,store.size&format=json")
res = conn.getresponse()
if res.status != 200 :
    raise Exception("unable to connect")

data = json.loads(res.read())

idx = [
    (v['index'], datetime.datetime.strptime(re.sub(r"^.*(\d{4}\.\d{2}\.\d{2})$", r"\1", v['index']), "%Y.%m.%d").date())
    for v in data
    if re.search(r"\d{4}\.\d{2}\.\d{2}$", v['index'])]
idx = [v for v in idx if (datetime.date.today() - v[1]).days > c.days]
for i in idx:
    print "removing %s" % i[0]
    conn.request("DELETE", "/%s/" % i[0])
    res = conn.getresponse()
    res.read()
    print res.status
