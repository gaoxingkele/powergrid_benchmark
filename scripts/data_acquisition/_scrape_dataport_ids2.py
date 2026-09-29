# -*- coding: utf-8 -*-
import re
import urllib.request

PROXY = "http://127.0.0.1:17890"
UA = "powergrid-benchmark/1.0"
pages = {
    "fo_ksv8": "https://ieee-dataport.org/documents/power-system-forced-oscillation-datasets",
    "testcases": "https://ieee-dataport.org/documents/test-cases-library-forcedsustained-power-system-oscillations",
}
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
for name, url in pages.items():
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = opener.open(req, timeout=90).read().decode("utf-8", "replace")
    ids = set(re.findall(r"/(?:data|open|docs|scripts)/(\d{6,7})/", html))
    s3 = set(re.findall(r"ieee-dataport\.s3\.amazonaws\.com/([^\"?]+)", html))
    print("===", name, "ids", sorted(ids))
    for x in sorted(s3)[:15]:
        print(" ", x[:120])
