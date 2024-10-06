# iphone_actions.py
# Moving the code related to "MacBook" and "iPhone" into separate functions or modules
# and then call those functions in your pytest test file.
# This will make the code cleaner and more modular.

import logging

logger = logging.getLogger()


def handle_iphone(page):
    """
    Handle actions related to iPhone 16 Pro Max.has_text="256GB Footnote ² From $1099"
    """
    logger.info("Handling iPhone 16 Pro Max actions.")
    page.wait_for_timeout(5000)
    # page.wait_for_timeout(10000)
    # page.locator("section").filter(has_text="iPhone 16 Pro Hello, Apple").get_by_label("Buy iPhone 16 Pro").click()
    page.locator("section:has-text('iPhone 16 Pro Hello, Apple')").locator('a[aria-label="Buy iPhone 16 Pro"]').nth(0).click()
    page.locator("label").filter(has_text="iPhone 16 Pro 6.3-inch").click()
    page.locator("label").filter(has_text="Desert Titanium").locator("img").click()
    page.locator("label").filter(has_text="256GB Footnote ² From $1099").click()
    page.locator("#noTradeIn_label").click()
    page.get_by_text("Buy$1,099.00Pay with Apple").click()
    page.get_by_text("Connect to any carrier later$").click()
    page.locator("#applecareplus_58_noapplecare_label").click()
    page.get_by_role("button", name="Add to Bag").click()
    page.wait_for_timeout(5000)
    page.screenshot(path='screenshots/iPhone 16 Pro Max.png')
    logger.info("Screenshot of iPhone 16 Pro Max taken.")
