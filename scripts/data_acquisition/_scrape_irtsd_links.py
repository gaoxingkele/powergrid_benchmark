# -*- coding: utf-8 -*-
import re
import urllib.request

PROXY = "http://127.0.0.1:17890"
UA = "powergrid-benchmark/1.0"
url = "https://ieee-dataport.org/open-access/irtsd-open-source-data-and-toolset-electromagnetic-transient-analysis-disturbances-and"
req = urllib.request.Request(url, headers={"User-Agent": UA})
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
html = opener.open(req, timeout=90).read().decode("utf-8", "replace")
for m in re.findall(r'href="([^"]+)"', html):
    if any(x in m.lower() for x in ["download", ".zip", "s3", "amazonaws", "event"]):
        print(m)
