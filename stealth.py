def apply_stealth(page):
    """
    Lightweight stealth tweaks: override navigator.webdriver, languages, plugins.
    Not a full fingerprinting mitigation — use with proxies/residential IPs.
    """
    page.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
        """
    )