import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "scraped"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_filename(url: str) -> str:
    """Create a safe filename from a URL."""
    parsed = urlparse(url)

    path_name = parsed.path.strip("/").replace("/", "_")
    name = path_name or parsed.netloc

    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return f"{name[:80]}.json"


def scrape_scheme_page(url: str, scheme_name: str) -> Path:
    """Scrape readable text from an official government scheme webpage."""

    if not url.startswith(("https://", "http://")):
        raise ValueError("A valid HTTP or HTTPS URL is required.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        )

        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60_000
            )

            page.wait_for_timeout(3000)

            title = page.title()

            text = page.locator("body").inner_text(timeout=30_000)

            # Remove excessive empty lines and spaces.
            lines = [
                re.sub(r"\s+", " ", line).strip()
                for line in text.splitlines()
            ]

            cleaned_text = "\n".join(
                line for line in lines
                if line and len(line) > 2
            )

            result = {
                "scheme_name": scheme_name,
                "title": title,
                "source_url": url,
                "source_type": "government_webpage",
                "scraped_at": datetime.now().isoformat(),
                "content": cleaned_text,
            }

            output_file = OUTPUT_DIR / create_filename(url)

            with output_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(result, file, ensure_ascii=False, indent=2)

            print(f"Saved: {output_file}")
            return output_file

        finally:
            browser.close()


if __name__ == "__main__":
    scheme_url = input("Enter official scheme URL: ").strip()
    scheme_name = input("Enter scheme name: ").strip()

    try:
        scrape_scheme_page(scheme_url, scheme_name)
    except Exception as error:
        print(f"Scraping failed: {error}")