# conftest.py
import pytest
from playwright.sync_api import Playwright, sync_playwright

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="function")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)  # Ustaw headless=True dla trybu bez interfejsu
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()