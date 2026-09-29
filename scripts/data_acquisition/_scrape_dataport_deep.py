# -*- coding: utf-8 -*-
import re
import urllib.request

PROXY = "http://127.0.0.1:17890"
UA = "powergrid-benchmark/1.0"
pages = {
    "fo": "https://ieee-dataport.org/documents/power-system-forced-oscillation-datasets",
    "tc": "https://ieee-dataport.org/documents/test-cases-library-forcedsustained-power-system-oscillations",
    "irtsd": "https://ieee-dataport.org/open-access/irtsd-open-source-data-and-toolset-electromagnetic-transient-analysis-disturbances-and",
}
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
for name, url in pages.items():
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = opener.open(req, timeout=90).read().decode("utf-8", "replace")
    print("===", name)
    for pat in [r"data/(\d+)/(\d+)", r"open/[a-z]+/(\d+)", r"datasetId[\"':=\s]+(\d+)", r"field_dataset_id[^0-9]+(\d+)"]:
        m = sorted(set(re.findall(pat, html)))
        if m:
            print(pat, m[:30])
    for line in html.splitlines():
        if "s3.amazonaws.com" in line and (".zip" in line.lower() or "event" in line.lower() or "fo_" in line.lower()):
            print(line.strip()[:200])
