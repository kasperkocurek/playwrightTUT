# Test.py
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://bookcart.azurewebsites.net/"

@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    """Fixture do otwarcia strony przed każdym testem."""
    page.goto(BASE_URL)
    yield

def test_page_title(page: Page):
    # Przejdź do strony
    page.goto("https://bookcart.azurewebsites.net/")

    # Dodaj pierwszy produkt do koszyka
    page.locator("mat-card-content").filter(has_text="Harry Potter and the Chamber of Secrets").get_by_role("button",
                                                                                                            name="Add to Cart").click()

    # Dodaj drugi produkt do koszyka
    page.locator("mat-card-content").filter(has_text="Harry Potter and the Prisoner of Azkaban").get_by_role("button",
                                                                                                             name="Add to Cart").click()

    # Przejdź do koszyka
    page.get_by_role("button", name="shopping_cart").click()

    # Sprawdź, czy koszyk zawiera dodane produkty
    expect(page.get_by_role("cell", name="Harry Potter and the Chamber of Secrets")).to_be_visible()
    expect(page.get_by_role("cell", name="Harry Potter and the Prisoner of Azkaban")).to_be_visible()

def test_login(page: Page):
    """Test logowania użytkownika."""
    page.click("text=Login")
    page.fill("input[placeholder='Username']", "testuser")
    page.fill("input[placeholder='Password']", "testpassword")
    page.click("button:text('Login')")
    expect(page.locator("text=testuser")).to_be_visible()

def test_search_books(page: Page):
    """Test wyszukiwania książek."""
    page.fill("input[placeholder='Search books or authors']", "The")
    page.press("input[placeholder='Search books or authors']", "Enter")
    expect(page.locator(".mat-card-title")).to_contain_text("The")

def test_add_to_cart(page: Page):
    """Test dodawania książki do koszyka."""
    page.fill("input[placeholder='Search books or authors']", "The")
    page.press("input[placeholder='Search books or authors']", "Enter")
    first_book = page.locator(".mat-card-title").first
    first_book.click()
    page.click("button:text('Add to Cart')")
    page.click("text=Cart")
    expect(page.locator(".mat-card-title")).to_contain_text(first_book.inner_text())

def test_remove_from_cart(page: Page):
    """Test usuwania książki z koszyka."""
    test_add_to_cart(page)
    page.click("text=Cart")
    page.click("button:text('Remove')")
    expect(page.locator("text=Your cart is empty")).to_be_visible()

def test_logout(page: Page):
    """Test wylogowania użytkownika."""
    test_login(page)
    page.click("text=Logout")
    expect(page.locator("text=Login")).to_be_visible()