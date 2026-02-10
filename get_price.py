import re
from typing import Optional, Union
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

prices = 0  # Global prices variable to store the number of price fetches for user agent rotation


def _extract_shop(link: str) -> Optional[str]:
    """Return the core shop name from a URL (e.g., amazon, playstation)."""

    hostname = urlparse(link).hostname
    if not hostname:
        return None

    parts = hostname.split(".")
    if len(parts) < 2:
        return None

    core = parts[-2]  # amazon.ca -> amazon, store.playstation.com -> playstation
    if core in {"amazon", "playstation"}:  # add more shops as needed
        return core

    return None


def amazon(parser: BeautifulSoup) -> Optional[float]:
    """
    Gets the price for amazon link

    :param parser: BeautifulSoup
    :type parser: BeautifulSoup
    :return: price of the product
    :rtype: float | None
    """
    try:
        # Amazon renders multiple price spans; the first a-offscreen is typically the main price
        price_span = parser.select_one("span.a-offscreen")
        if not price_span:
            return None

        price_text = price_span.text.strip()
        price_text = re.sub(r"[^0-9.,]", "", price_text)
        price_text = price_text.replace(",", "")
        return float(price_text)
    except Exception:
        return None


def playstation(parser: BeautifulSoup) -> Union[int, float, None]:
    """
    Extract price from PlayStation Store pages.

    :param parser: BeautifulSoup
    :type parser: BeautifulSoup
    :return: price of the product
    :rtype: int | float | None
    """

    try:
        # Primary selector used by the PlayStation Store CTA price element
        price_node = parser.select_one('[data-qa*="finalPrice"]')
        if not price_node:
            # Fallback to schema.org price meta
            price_node = parser.select_one('[itemprop="price"]')

        if not price_node:
            return None

        # Some nodes are meta tags
        price_text = price_node.get("content") or price_node.text
        price_text = price_text.strip()
        match = re.search(r"([0-9]+[.,][0-9]{2})", price_text)
        if not match:
            return None

        normalized = match.group(1).replace(",", "")
        return float(normalized)
    except Exception:
        return None


# Add more shop function below as needed (e.g., Walmart, Best Buy, etc.)


def get_price(link: str) -> Union[int, float, None]:
    """
    Return the product price for an Amazon or PlayStation link.

    :param link: URL of the product page
    :type link: str
    :return: price of the product
    :rtype: int | float | None
    """

    global prices  # Use the global prices variable for user agent rotation

    shop = _extract_shop(link)
    shops = {
        "amazon": amazon,
        "playstation": playstation,
        # add more shops as needed
    }

    if not shop or shop not in shops:
        print("Link is not from the allowed shops!")
        print(f"Allow list: {list(shops.keys())}")
        return None

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; en-US) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edge/80.0.361.109",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    ]

    headers = {
        "User-Agent": user_agents[prices % len(user_agents)],
        "Accept-Language": "en-US,en;q=0.9",
    }
    prices += 1

    try:
        res = requests.get(link, headers=headers, timeout=15)
        res.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to fetch page: {exc}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    return shops[shop](soup)
