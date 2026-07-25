from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)  # opens a Safari/WebKit-based browser
    page = browser.new_page()
    page.goto("https://www.google.com")
    page.screenshot(path="google.png")
    browser.close()
