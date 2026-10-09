from pytest_bdd import given, when, then
from pages.login_page import LoginPage
from pages.add_to_cart import AddToCart
import os as OS

@given("I am logged in to the application")
def logged_in(page, base_url):
    login_page = LoginPage(page)
    page.goto(base_url)
    login_page.click_login_link()
    login_page.enter_username(OS.getenv("VALID_USERNAME"))
    login_page.enter_password(OS.getenv("VALID_PASSWORD"))
    login_page.click_login_button()
    page.wait_for_timeout(5000)  # Wait for 5 seconds to allow the login process to complete


@when("I click on a product")
def click_product(page):
    add_to_cart_page = AddToCart(page)
    add_to_cart_page.click_product()
    page.wait_for_timeout(2000)  # Wait for 2 seconds to allow the product page to load

@when("I click on the Add to cart button")
def click_add_to_cart(page):
    add_to_cart_page = AddToCart(page)
    add_to_cart_page.click_add_to_cart()
    page.wait_for_timeout(2000)  # Wait for 2 seconds to allow the add to cart process to complete

@when("I click on the Cart button")
def click_cart(page):
    add_to_cart_page = AddToCart(page)
    add_to_cart_page.click_cart()
    page.wait_for_timeout(5000)  # Wait for 2 seconds to allow the cart page to load

@then("I should see the added product in the cart")
def verify_product_in_cart(page):
    add_to_cart_page = AddToCart(page)
    # Verify that the product is present in the cart
    assert add_to_cart_page.verify_product_in_cart(), "Product is not present in the cart."