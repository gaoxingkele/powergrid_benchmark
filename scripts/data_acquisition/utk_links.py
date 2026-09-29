import re
import urllib.request

for page in [
    "http://web.eecs.utk.edu/~kaisun/Oscillation/contestcases.html",
    "http://web.eecs.utk.edu/~kaisun/Oscillation/simulatedcases.html",
]:
    html = urllib.request.urlopen(page, timeout=60).read().decode("utf-8", "replace")
    print("===", page)
    for m in re.findall(r'href="([^"]+)"', html):
        if ".zip" in m.lower() or "All" in m:
            print(m)
