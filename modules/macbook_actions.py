# macbook_actions.py
# Moving the code related to "MacBook" and "iPhone" into separate functions or modules
# and then call those functions in your pytest test file.
# This will make the code cleaner and more modular.
import logging

logger = logging.getLogger()


def handle_macbook(page):
    """
    Handle actions related to MacBook Pro.
    """
    logger.info("Handling MacBook Pro actions.")
    page.locator("section").filter(has_text="MacBook Pro Mind-blowing.Head").get_by_label("Buy, MacBook Pro").click()
    page.get_by_role("radio", name="16-inch").click()
    page.get_by_role("tab", name="M3 Pro").click()
    page.get_by_role("button", name="Select Apple M3 Pro with 12-").nth(1).click()
    page.get_by_role("button", name="Add to Bag").click()
    page.wait_for_timeout(5000)
    page.screenshot(path='screenshots/MacBook_Pro.png')
    logger.info("Screenshot of MacBook Pro taken.")
