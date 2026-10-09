from pytest_bdd import given, when, then
from pages.login_page import LoginPage
import os as OS


# =========================
# Background
# =========================

@given("user is on the Demoblaze application")
def open_application(page, base_url):
    page.goto(base_url)


# =========================
# Valid Login
# =========================

@when("users open the login dialog")
def open_login_dialog(page):
    login_page = LoginPage(page)
    login_page.click_login_link()


@when("user enters the valid username and password")
def enter_valid_credentials(page):
    login_page = LoginPage(page)

    login_page.enter_username(OS.getenv("VALID_USERNAME"))
    login_page.enter_password(OS.getenv("VALID_PASSWORD"))


@when("user clicks the login button")
def click_login_button(page):
    login_page = LoginPage(page)

    login_page.click_login_button()
    page.wait_for_timeout(10000) # Wait for 5 seconds to allow the login process to complete


@then("user should be logged in successfully")
def verify_successful_login(page):
    login_page = LoginPage(page)

    assert login_page.is_logout_visible(), \
        "Logout button is not visible. Login failed."


# =========================
# Invalid Login
# =========================

@when("user enters the invalid username and password")
def enter_invalid_credentials(page):
    login_page = LoginPage(page)

    login_page.enter_username(OS.getenv("INVALID_USERNAME"))
    login_page.enter_password(OS.getenv("INVALID_PASSWORD"))


@when("user clicks the login button with invalid credentials")
def click_login_button_with_invalid_credentials(page):
    login_page = LoginPage(page)

    with page.expect_event("dialog") as dialog_info:
        login_page.click_login_button()

    dialog = dialog_info.value

    page.dialog_message = dialog.message

    dialog.accept()


@then("login should fails with an error message")
def verify_login_error(page):
    assert page.dialog_message == "User does not exist.", \
        f"Unexpected error message: {page.dialog_message}"