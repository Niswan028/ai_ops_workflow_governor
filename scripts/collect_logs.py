import csv
import asyncio
from datetime import datetime, timezone
from playwright.async_api import async_playwright

SITE_URL = "https://fitaichat.netlify.app"
PAGES = ["/", "/chat"]
OUTPUT = "data/performance_logs.csv"


async def collect(page_path: str, browser):
    url = SITE_URL + page_path
    page = await browser.new_page()

    # capture performance timing via JS
    await page.goto(url, wait_until="networkidle")
    timing = await page.evaluate("""() => {
        const t = performance.timing;
        return {
            ttfb: t.responseStart - t.requestStart,
            load_time: t.loadEventEnd - t.navigationStart,
            requests: performance.getEntriesByType('resource').length
        }
    }""")

    # simple CWV status based on load time
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


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        rows = [await collect(path, browser) for path in PAGES]
        await browser.close()

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[Collector] {len(rows)} row(s) written to {OUTPUT}")
    for r in rows:
        print(f"  {r['page_url']} -> load={r['load_time_ms']}ms, ttfb={r['ttfb_ms']}ms, requests={r['requests_count']}, status={r['core_web_vitals_status']}")


asyncio.run(main())
