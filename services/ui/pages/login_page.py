from .base_page import BasePage
from services import MAIL_URL
from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_email = None
        self.password_field = None
        self.login_button = None

    def open(self):
        self.page.goto(MAIL_URL)

    def login(self, username: str, password: str):
        """
        Метод для авторизации на сайте
        :param username: Логин в виде email
        :param password: Пароль
        """
        self.clickable(self.username_email)
        self.page.type(self.username_email, username)
        self.clickable(self.password_field)
        self.page.type(self.password_field, password)
        self.clickable(self.login_button)
        self.page.click(self.login_button)
