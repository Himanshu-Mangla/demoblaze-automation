from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, value):
        self.page.locator(locator).fill(value)

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def get_text(self, locator):
        return self.page.locator(locator).inner_text()

    def get_title(self):
        return self.page.title()

    def navigate(self, url):
        self.page.goto(url)

    

