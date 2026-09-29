# -*- coding: utf-8 -*-
import re
import urllib.request

UA = "powergrid-benchmark/1.0"
pages = [
    "http://web.eecs.utk.edu/~kaisun/Oscillation/simulatedcases.html",
    "http://web.eecs.utk.edu/~kaisun/Oscillation/contestcases.html",
    "https://web.eecs.utk.edu/~kaisun/Oscillation/2021Contest/",
]
for url in pages:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    print("===", url)
    for m in re.findall(r'href="([^"]+)"', html):
        if any(x in m.lower() for x in [".zip", "download", "all"]):
            print(m)
