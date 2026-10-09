from pages.base_page import BasePage


class LoginPage(BasePage):

    LOGIN_LINK = "#login2"
    USERNAME_FIELD = "#loginusername"
    PASSWORD_FIELD = "#loginpassword"
    LOGOUT_BUTTON = "#logout2"

    def click_login_link(self):
        self.click(self.LOGIN_LINK)

    def enter_username(self, username):
        self.fill(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        self.fill(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        self.page.get_by_role("button", name="Log in").click()

    def is_logout_visible(self):
        return self.is_visible(self.LOGOUT_BUTTON)

    def click_logout_button(self):
        self.click(self.LOGOUT_BUTTON)