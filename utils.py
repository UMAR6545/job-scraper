import csv
import json
import logging
import random
import re
import time
from pathlib import Path
from typing import Optional, List

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    # add more UAs for better rotation
]
DEFAULT_WAIT_RANGE = (5, 12)
logging.getLogger().setLevel(logging.INFO)


def choose_user_agent() -> str:
    return random.choice(USER_AGENTS)


def random_sleep(wait_range: tuple = DEFAULT_WAIT_RANGE):
    t = random.uniform(*wait_range)
    logging.debug(f"Sleeping {t:.2f}s")
    time.sleep(t)


def safe_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    s = re.sub(r"\s+", " ", text).strip()
    return s if s else None


def load_proxies(file_path: Optional[str]) -> List[str]:
    # returns list of proxy strings (e.g. http://user:pass@host:port)
    if not file_path:
        return []
    p = Path(file_path)
    if not p.exists():
        logging.warning("Proxy file not found: %s", file_path)
        return []
    with p.open("r", encoding="utf-8") as f:
        proxies = [ln.strip() for ln in f if ln.strip()]
    return proxies


def write_output(records: list, out_path: str):
    p = Path(out_path)
    if p.suffix.lower() == ".csv":
        if not records:
            Path(out_path).write_text("")  # create empty file
            return
        with p.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            for r in records:
                writer.writerow(r)
        logging.info("Wrote CSV to %s", out_path)
    else:
        with p.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        logging.info("Wrote JSON to %s", out_path)
