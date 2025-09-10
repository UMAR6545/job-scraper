import argparse
import logging
import random

from playwright.sync_api import sync_playwright

from scrapers.indeed import IndeedScraper
from utils import load_proxies, choose_user_agent, write_output


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--site", choices=["indeed", "all"], default="all")
    p.add_argument("--designation", required=True)
    p.add_argument("--skills", default="")
    p.add_argument("--location", required=True)
    p.add_argument("--out", default="out.json")
    p.add_argument("--proxy-file", default=None)
    p.add_argument("--headless", action="store_true", help="Run headless; by default runs headed for easier demo")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--debug", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    proxies = load_proxies(args.proxy_file)
    selected_proxy = random.choice(proxies) if proxies else None
    logging.info("Using proxy: %s", selected_proxy)
    scraper_classes = []
    if args.site in ("indeed", "all"):
        scraper_classes.append(IndeedScraper)
    results = []
    with sync_playwright() as playwright:
        for cls in scraper_classes:
            user_agent = choose_user_agent()
            scraper = cls(args.designation, args.skills, args.location, headless=args.headless)
            try:
                logging.info("Running %s (UA: %s)", cls.__name__, user_agent)
                recs = scraper.search(playwright, user_agent, selected_proxy)
                results.extend(recs)
                logging.info("Got %d records from %s", len(recs), cls.__name__)
                # if len(results) >= args.limit:
                #     break
            except Exception as e:
                logging.exception("Scraper %s failed: %s", cls.__name__, e)

    write_output(results, args.out)
    logging.info("Scraping finished, total records: %d", len(results))


if __name__ == "__main__":
    main()
