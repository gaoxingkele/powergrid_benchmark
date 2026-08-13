"""Fail-closed statistical surface for the runtime compatibility package."""


def mannwhitneyu(*args, **kwargs):  # type: ignore[no-untyped-def]
    raise RuntimeError(
        "Statistical inference is disabled in the p5_s3 SciPy compatibility "
        "surface; this stage reports prespecified descriptive sensitivity only."
    )


def gmean(*args, **kwargs):  # type: ignore[no-untyped-def]
    raise RuntimeError("gmean is outside the p5_s3 compatibility surface")

