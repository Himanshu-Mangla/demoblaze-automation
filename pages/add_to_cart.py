from pages.base_page import BasePage

class AddToCart(BasePage):

    PRODUCT = ".card-title"
    ADD_TO_CART_BUTTON = "Add to cart"
    CART_LINK = "#cartur"
    VERIFY_PRODUCT_IN_CART = ".success"

    def click_product(self):
        self.page.locator(self.PRODUCT).first.click()

    def click_add_to_cart(self):
        self.page.get_by_role("link", name=self.ADD_TO_CART_BUTTON).click()
        self.page.once("dialog", lambda dialog: dialog.accept())

    def click_cart(self):
        self.page.locator(self.CART_LINK).click()

    def verify_product_in_cart(self):
        return self.page.locator(self.VERIFY_PRODUCT_IN_CART).is_visible()

