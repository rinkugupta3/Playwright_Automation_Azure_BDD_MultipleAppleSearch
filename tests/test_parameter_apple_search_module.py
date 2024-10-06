"""
Project Description:

This project automates the process of searching for Apple products on the Apple website, adding them to the shopping bag, reviewing the items, removing them from the bag, and returning to the homepage using Playwright for browser automation and pytest-bdd for Behavior Driven Development (BDD) testing.

The project includes the following components:

1. **Test Script (this file)**:
   - Contains the automated test scenarios written in BDD style using `pytest-bdd`.
   - Executes actions like visiting the Apple homepage, searching for products (e.g., MacBook Pro and iPhone 16 Pro), adding products to the bag, reviewing them, removing them from the bag, and returning to the homepage.

2. **Feature File**:
   - Located separately, the feature file defines the test scenarios in Gherkin syntax. These scenarios describe the expected behavior, such as searching for products, adding them to the bag, and taking screenshots.

3. **Module Files**:
   - `macbook_actions.py`, `iphone_actions.py`, and `remove_product_from_bag.py`: These modular scripts handle the specific actions for each product, such as adding to the cart or removing from the bag, ensuring clean and reusable code.

4. **Config File**:
   - `config.py`: Contains configuration settings such as URLs, making the script adaptable for different environments.

Key Features:
- Utilizes Playwright's `sync_api` for reliable browser interactions.
- Implements robust error handling and fallbacks, such as direct navigation to the homepage if the Apple logo link is not clickable.
- Log output with timestamps to track test execution details.
- Dynamic screenshot capture for each product at key points in the test flow (search results, product review).
- BDD structure makes the test cases easy to understand and maintain.
"""

# Headless mode is set to True and test will run across multiple browsers (Chromium, Firefox, WebKit)
# pytest -s -v tests/test_parameter_apple_search_module.py
# pytest -s -v tests/test_parameter_apple_search_module.py --html=report.html


import logging
import os
import pytest
from playwright.sync_api import Page, Playwright
from pytest_bdd import scenarios, given, when, then, parsers
from config.config import Config
from modules.macbook_actions import handle_macbook  # Import MacBook actions
from modules.iphone_actions import handle_iphone  # Import iPhone actions
from modules.remove_product_from_bag import handle_remove_product  # Import remove product from bag

# Set up logging with timestamps for detailed logs
log_file = 'test_results.txt'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",  # Include timestamp in the log messages
    datefmt="%Y-%m-%d %H:%M:%S",  # Format for the timestamp
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Load the feature file
scenarios('../features/parameter.feature')

# Ensure the screenshots directory exists
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')


@pytest.fixture(scope="session")
def browser_setup(playwright: Playwright):
    # Check if running in CI/CD environment and set headless mode accordingly
    headless = os.getenv('HEADLESS', 'false').lower() == 'true'

    logger.info(f"Launching browser in {'headless' if headless else 'headed'} mode.")
    browser = playwright.chromium.launch(headless=headless)  # Set headless mode based on environment
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@given("I am on the Apple homepage")
def visit_apple_com(browser_setup: Page):
    page = browser_setup
    page.goto(Config.HOMEPAGE_URL)
    page.wait_for_load_state("networkidle")
    page.screenshot(path='screenshots/homepage.png')
    logger.info("Visited Apple homepage")


@when(parsers.parse("I search for {product}"))
def search_for_product(browser_setup: Page, product):
    logger.info(f"Searching for {product}")
    page = browser_setup
    page.wait_for_load_state("networkidle")

    search_button = page.get_by_role("button", name="Search apple.com")
    search_button.click()
    search_input = page.get_by_placeholder("Search apple.com")
    search_input.fill(product)
    search_input.press("Enter")

    # Wait for search results to load
    page.wait_for_selector('text="Search Results"', timeout=10000)
    page.wait_for_load_state("networkidle")

    # Take a screenshot after performing the search
    product_name_for_file = product.replace('"', '').replace("'", "").replace(" ", "_")
    page.screenshot(path=f'screenshots/search_results_for_{product_name_for_file}.png')

    # Navigate to the product page based on search results
    # product_name = ""
    if "MacBook Pro" in product:
        product_name = "MacBook Pro - Apple"
    elif "iPhone" in product:
        product_name = "iPhone 16 Pro and iPhone 16 Pro Max - Apple"
    else:
        raise ValueError(f"Product '{product}' is not handled in the script.")

    # Click the product link
    page.get_by_role("link", name=product_name, exact=True).click()
    page.wait_for_timeout(5000)


@when(parsers.parse("I add the first {product} result to the bag"))
def add_product_to_bag(browser_setup: Page, product):
    page = browser_setup
    # product = product

    if "MacBook Pro" in product:
        handle_macbook(page)  # Call the function for MacBook
    elif "iPhone" in product:
        handle_iphone(page)  # Call the function for iPhone
    else:
        raise ValueError(f"Product '{product}' not handled by the script.")


@then("I should be able to proceed to the review bag")
def proceed_to_review_bag(browser_setup: Page):
    page = browser_setup
    logger.info("Proceeding to review bag.")
    review_bag_button = page.get_by_role("button", name="Review Bag")
    review_bag_button.wait_for(state="visible", timeout=5000)
    review_bag_button.click()
    page.wait_for_load_state("networkidle")


@then(parsers.parse("a screenshot of the reviewed {product} should be taken"))
def take_screenshot_of_review(browser_setup: Page, product):
    page = browser_setup
    page.wait_for_load_state("networkidle")
    product_name_for_file = product.replace('"', '').replace("'", "").replace(" ", "_")
    screenshot_path = f'screenshots/reviewed_{product_name_for_file}.png'
    page.screenshot(path=screenshot_path)
    logger.info(f"Screenshot of the reviewed {product} taken at {screenshot_path}.")

    # page.wait_for_timeout(10000)


@then(parsers.parse('the "{product}" should be removed or deleted from the bag'))
def remove_product_from_bag(browser_setup: Page, product: str):
    page = browser_setup
    handle_remove_product(page, product)  # Pass the product name dynamically
    page.wait_for_timeout(2000)


@then("I return to the Apple homepage")
def return_to_homepage(browser_setup: Page):
    page = browser_setup
    page.wait_for_load_state("networkidle")
    try:
        # Wait for the Apple home page button to be clickable
        apple_home_page = page.wait_for_selector("a.globalnav-link-apple", state='visible', timeout=20000)
        # Click the Apple home page button
        apple_home_page.click()
        page.wait_for_load_state('load')  # Wait for the page to fully load
        page.wait_for_timeout(2000)
    except TimeoutError:
        # If the link is not clickable, fallback to direct navigation
        page.goto(Config.HOMEPAGE_URL)
        page.wait_for_load_state('load')  # Wait for the homepage to load


@then("I close the browser")
def close_browser(browser_setup: Page):
    logger.info("Closing the browser.")
    # The browser will be closed automatically by the fixture
