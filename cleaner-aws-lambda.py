from __future__ import print_function
import datetime
import httplib
import json
import re
import logging


c = dict()
c['host'] = 'localhost'
c['days'] = 1

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    conn = httplib.HTTPConnection(c['host'])
    conn.request("GET", "/_cat/indices?h=index,store.size&format=json")
    res = conn.getresponse()
    if res.status != 200:
        raise Exception("unable to connect to %s" % c['host'])

    data = json.loads(res.read())

    idx = [
        (v['index'], datetime.datetime.strptime(re.sub(r"^.*(\d{4}\.\d{2}\.\d{2})$", r"\1", v['index']), "%Y.%m.%d").date())
        for v in data
        if re.search(r"\d{4}\.\d{2}\.\d{2}$", v['index'])]
    idx = [v for v in idx if (datetime.date.today() - v[1]).days > c['days']]
    for i in idx:
        logger.info("removing %s" % i[0])
        conn.request("DELETE", "/%s/" % i[0])
        res = conn.getresponse()
        res.read()
        logger.info(res.status)
    return "ok"
