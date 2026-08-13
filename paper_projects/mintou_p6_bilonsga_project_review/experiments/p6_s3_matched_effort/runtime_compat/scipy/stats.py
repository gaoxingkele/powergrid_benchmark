"""Fail-closed placeholder for the shared module's unused legacy import."""


def mannwhitneyu(*args, **kwargs):  # type: ignore[no-untyped-def]
    raise RuntimeError(
        "Mann-Whitney inference is disabled in the P6 S3 compatibility surface; "
        "the stage runner implements its declared exact paired sign test directly."
    )

