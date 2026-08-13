"""Import-only placeholder for pymoo termination modules.

The selected runs use an explicit generation-count termination and the stage's
separate exact hypervolume helper. Pymoo imports its HV termination module while
building the algorithm even though that termination is not selected. Any actual
attempt to call this placeholder fails closed.
"""

__version__ = "import-only-p5-s3"


def hypervolume(*args, **kwargs):  # type: ignore[no-untyped-def]
    raise RuntimeError(
        "pymoo's moocore indicator is outside the selected generation-count "
        "termination; use the p5_s3 exact hypervolume helper"
    )
