import logging
from typing import Optional

from stealth import apply_stealth
from utils import random_sleep


class BaseScraper:
    def __init__(self, designation: str, skills: str, location: str, headless: bool = True):
        self.designation = designation
        self.skills = skills
        self.location = location
        self.headless = headless

    def _launch(self, playwright, user_agent: str, proxy: Optional[str]):
        """
        Launches browser and returns (browser, context, page).
        proxy: string like 'http://user:pass@host:port' or 'http://host:port' or None
        """
        chromium = playwright.chromium
        browser = chromium.launch(headless=self.headless)
        ctx_kwargs = {"locale": "en-US", "user_agent": user_agent}
        if proxy:
            ctx_kwargs["proxy"] = {"server": proxy}
        context = browser.new_context(**ctx_kwargs)
        page = context.new_page()
        page.set_default_timeout(30000)
        apply_stealth(page)
        # small initial wait to mimic human
        random_sleep()
        logging.debug("Launched browser context (headless=%s proxy=%s)", self.headless, proxy)
        return browser, context, page
