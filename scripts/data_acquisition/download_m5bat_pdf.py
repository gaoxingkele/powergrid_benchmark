"""Download M5BAT report PDF after challenge cookie is established."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("data/public_datasets/bess_grid/m5bat_bess")
PDF = OUT / "Report_04-2023.pdf"
PROXY = "http://127.0.0.1:17890"
if PDF.exists() and PDF.stat().st_size < 10_000:
    PDF.unlink()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, proxy={"server": PROXY})
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    page.goto(
        "https://publications.rwth-aachen.de/record/985923",
        wait_until="domcontentloaded",
        timeout=120_000,
    )
    page.wait_for_timeout(3000)
    with page.expect_download(timeout=120_000) as dl_info:
        try:
            page.evaluate(
                "window.location.href='https://publications.rwth-aachen.de/record/985923/files/Report_04-2023.pdf'"
            )
        except Exception:
            pass
    download = dl_info.value
    download.save_as(str(PDF))
    browser.close()

print(PDF, PDF.stat().st_size if PDF.exists() else 0)
raise SystemExit(0 if PDF.exists() and PDF.stat().st_size > 100_000 else 1)
