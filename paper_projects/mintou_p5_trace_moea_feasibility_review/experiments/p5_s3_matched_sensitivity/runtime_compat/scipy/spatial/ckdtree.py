"""Fail-closed placeholder; cKDTree is not used by the selected methods."""


class cKDTree:  # noqa: N801
    def __init__(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("cKDTree is outside the p5_s3 compatibility surface")

