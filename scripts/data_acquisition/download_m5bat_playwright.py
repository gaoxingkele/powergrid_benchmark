"""Download M5BAT via Chromium to pass RWTH fast-challenge JS gate."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("data/public_datasets/bess_grid/m5bat_bess")
OUT.mkdir(parents=True, exist_ok=True)
ZIP = OUT / "M5BAT_04-2023_RAW.zip"
PDF = OUT / "Report_04-2023.pdf"
PROXY = "http://127.0.0.1:17890"

# remove challenge placeholders
for p in [ZIP, PDF]:
    if p.exists() and p.stat().st_size < 10_000:
        p.unlink()

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        proxy={"server": PROXY},
        args=["--ignore-certificate-errors"],
    )
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    print("open record page...", flush=True)
    page.goto(
        "https://publications.rwth-aachen.de/record/985923",
        wait_until="networkidle",
        timeout=120_000,
    )
    page.wait_for_timeout(5000)
    html = page.content()
    (OUT / "record_playwright.html").write_text(html, encoding="utf-8")
    print("page len", len(html), "title", page.title(), flush=True)

    # Download zip
    print("download zip...", flush=True)
    with page.expect_download(timeout=180_000) as dl_info:
        page.goto(
            "https://publications.rwth-aachen.de/record/985923/files/M5BAT_04-2023_RAW.zip",
            wait_until="commit",
            timeout=180_000,
        )
    download = dl_info.value
    download.save_as(str(ZIP))
    print("zip saved", ZIP, ZIP.stat().st_size, flush=True)

    print("download pdf...", flush=True)
    with page.expect_download(timeout=120_000) as dl_info2:
        page.goto(
            "https://publications.rwth-aachen.de/record/985923/files/Report_04-2023.pdf",
            wait_until="commit",
            timeout=120_000,
        )
    download2 = dl_info2.value
    download2.save_as(str(PDF))
    print("pdf saved", PDF, PDF.stat().st_size, flush=True)
    browser.close()

ok = ZIP.exists() and ZIP.stat().st_size > 50_000_000
print("SUCCESS" if ok else "FAIL", flush=True)
raise SystemExit(0 if ok else 1)
