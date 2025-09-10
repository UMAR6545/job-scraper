from model import JobRecord
from scrapers.base import BaseScraper
from typing import List, Optional
import time
import logging

from utils import random_sleep, safe_text


class IndeedScraper(BaseScraper):
    BASE = "https://pk.indeed.com"

    def _build_search_url(self) -> str:
        q = self.skills
        l = "+".join(self.location.split())
        return f"{self.BASE}/jobs?q={q}&l={l}"

    def search(self, playwright, user_agent: str, proxy: Optional[str]):
        browser, context, page = self._launch(playwright, user_agent, proxy)
        records: List[JobRecord] = []
        try:
            url = self._build_search_url()
            logging.info("Indeed: opening %s", url)
            page.goto(url, wait_until="domcontentloaded")
            random_sleep()
            # accept cookie banner if needed
            try:
                page.locator("button:has-text('Accept'), button:has-text('I agree')").first.click(timeout=2000)
            except Exception:
                pass
            cards = page.locator("a.tapItem, div.job_seen_beacon, div.jobsearch-SerpJobCard")
            if cards.count() == 0:
                logging.info("Indeed: no job cards found (selectors may need update)")
                return records

            total = cards.count()
            logging.info("Indeed: found %d job cards (iterating up to 40)", total)
            for i in range(min(total, 40)):
                try:
                    card = cards.nth(i)
                    title = safe_text(card.locator("h2.jobTitle, .jobTitle").inner_text(timeout=1500))
                    company = safe_text(card.locator('[data-testid="company-name"]').inner_text(timeout=1500))
                    loc = safe_text(card.locator('[data-testid="text-location"]').inner_text(timeout=1500))
                    a_tag = card.locator("a.tapItem").first

                    # extract href
                    a_tag = card.locator("h2.jobTitle a").first
                    href = a_tag.get_attribute("href")

                    job_url = f"{self.BASE}{href}" if href else None

                    rec = JobRecord(
                        site="Indeed",
                        job_title=title,
                        company_name=company,
                        location=loc,
                        job_url=job_url,
                        scraped_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    records.append(rec.as_dict())
                    random_sleep()

                except Exception as e:
                    logging.info("Indeed: card iteration error %s", e)
                    continue

        finally:
            try:
                context.close()
                browser.close()
            except Exception:
                pass
        return records

