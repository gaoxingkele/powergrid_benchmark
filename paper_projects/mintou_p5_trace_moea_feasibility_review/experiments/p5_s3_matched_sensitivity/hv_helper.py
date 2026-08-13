"""Line-oriented exact hypervolume helper for the free-threaded run process.

The installed pymoo 0.4.1 vendor module implements the Fonseca--Paquete--
Lopez-Ibanez dimension sweep in pure Python.  This helper is isolated from the
pymoo 0.6.2 optimizer source path and performs no optimization or statistics.
"""

from __future__ import annotations

import json
import sys

from pymoo.vendor.hv import HyperVolume


def main() -> None:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if request.get("command") == "close":
                return
            indicator = HyperVolume(request["reference"])
            value = float(indicator.compute(request["front"]))
            response = {"hypervolume": value}
        except Exception as exc:  # fail closed and return the concrete error
            response = {"error": f"{type(exc).__name__}: {exc}"}
        sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
