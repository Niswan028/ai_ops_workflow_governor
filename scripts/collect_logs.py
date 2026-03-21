import csv
import asyncio
import argparse
from datetime import datetime, timezone
from playwright.async_api import async_playwright

DEFAULT_SITE = "https://fitaichat.netlify.app"
DEFAULT_PAGES = ["/", "/chat"]
OUTPUT = "data/performance_logs.csv"


async def collect(page_path: str, browser, site_url: str):
    url = site_url + page_path
    page = await browser.new_page()
    await page.goto(url, wait_until="networkidle")
    timing = await page.evaluate("""() => {
        const t = performance.timing;
        return {
            ttfb: t.responseStart - t.requestStart,
            load_time: t.loadEventEnd - t.navigationStart,
            requests: performance.getEntriesByType('resource').length
        }
    }""")
    load = timing["load_time"]
    status = "good" if load < 1000 else "needs-improvement" if load < 2500 else "poor"
    await page.close()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "page_url": page_path,
        "ttfb_ms": timing["ttfb"],
        "load_time_ms": load,
        "requests_count": timing["requests"],
        "core_web_vitals_status": status,
    }


async def main(site_url: str, pages: list):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        rows = [await collect(path, browser, site_url) for path in pages]
        await browser.close()

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[Collector] {len(rows)} row(s) written to {OUTPUT}")
    for r in rows:
        print(f"  {r['page_url']} -> load={r['load_time_ms']}ms, ttfb={r['ttfb_ms']}ms, requests={r['requests_count']}, status={r['core_web_vitals_status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect performance metrics from a site")
    parser.add_argument("--site", default=DEFAULT_SITE, help="Base URL of the site")
    parser.add_argument("--pages", nargs="+", default=DEFAULT_PAGES, help="Pages to collect")
    args = parser.parse_args()
    asyncio.run(main(args.site, args.pages))
