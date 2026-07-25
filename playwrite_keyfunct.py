from playwright.sync_api import sync_playwright

browser = sync_playwright().start().webkit.launch(headless=False)  # opens a Safari/WebKit-based browser
page = browser.new_page()

page.goto("https://www.screener.in/company/NIFTY/#constituents")
page.screenshot(path="screener.png")

page.click("text=50")

browser.close()