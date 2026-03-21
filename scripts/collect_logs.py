import csv
import asyncio
import argparse
import os
from datetime import datetime, timezone
from playwright.async_api import async_playwright

DEFAULT_SITE = "https://hashnode.com"
DEFAULT_PAGES = ["/", "/explore", "/featured"]
OUTPUT = "data/performance_logs.csv"
HISTORY = "data/performance_logs_history.csv"


async def collect(page_path: str, browser, site_url: str):
    url = site_url + page_path
    page = await browser.new_page()

    slow_assets = []
    page.on("response", lambda r: slow_assets.append(r.url) if r.url.endswith((".js", ".css")) else None)

    start = asyncio.get_event_loop().time()
    response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(3000)
    load_time = int((asyncio.get_event_loop().time() - start) * 1000)

    ttfb = 0
    try:
        timing = await page.evaluate("""() => {
            const nav = performance.getEntriesByType('navigation')[0];
            return nav ? Math.round(nav.responseStart) : 0;
        }""")
        ttfb = timing
    except Exception:
        ttfb = 0

    requests_count = len(slow_assets)
    status = "good" if load_time < 1000 else "needs-improvement" if load_time < 2500 else "poor"
    await page.close()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "page_url": page_path,
        "ttfb_ms": ttfb,
        "load_time_ms": load_time,
        "requests_count": requests_count,
        "core_web_vitals_status": status,
        "detected_assets": "|".join(slow_assets[:5]),
    }


async def main(site_url: str, pages: list):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        rows = [await collect(path, browser, site_url) for path in pages]
        await browser.close()

    # overwrite current log
    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # append to history log
    write_header = not os.path.exists(HISTORY)
    with open(HISTORY, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(rows)

    print(f"[Collector] {len(rows)} row(s) written to {OUTPUT} and appended to {HISTORY}")
    for r in rows:
        print(f"  {r['page_url']} -> load={r['load_time_ms']}ms, ttfb={r['ttfb_ms']}ms, requests={r['requests_count']}, status={r['core_web_vitals_status']}")
        if r["detected_assets"]:
            print(f"    assets: {r['detected_assets']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect performance metrics from a site")
    parser.add_argument("--site", default=DEFAULT_SITE, help="Base URL of the site")
    parser.add_argument("--pages", nargs="+", default=DEFAULT_PAGES, help="Pages to collect")
    args = parser.parse_args()
    asyncio.run(main(args.site, args.pages))
