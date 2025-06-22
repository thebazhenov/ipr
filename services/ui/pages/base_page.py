from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def clickable(self, selector: str):
        if self.page.is_visible(selector) and self.page.is_enabled(selector):
            return True
        return False

