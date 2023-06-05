import typing

from playwright.sync_api import Locator, Page, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class AuthPage(BasePage):
    PATH = 'auth/signin'

    def __init__(self, page: Page, host: str):
        super().__init__(page=page, page_url=f'{host}/{self.PATH}')
        self.title: str = 'Smart Diagnostics'

    @property
    def logo(self) -> Locator:
        return self.locator('div[class*="AuthLayout_LogoContainer"]>span[class*="Icon_icon"]>svg')

    @property
    def login_input(self) -> Locator:
        return self.locator('//label[span[contains(.,"Логин")]]/div/input')

    @property
    def form_title_text(self) -> Locator:
        return self.locator('//div[@class[contains(.,"SignInForm_Header")]]/span[contains(.,"Войдите в свой аккаунт")]')

    @property
    def form_subtitle_text(self) -> Locator:
        return self.locator(
            '//div[@class[contains(.,"SignInForm_Header")]]/span[contains(.,"Введите ваш логин и пароль для входа")]')

    @property
    def login_input_title(self) -> Locator:
        return self.locator('//label[@class[contains(.,"Input_Input")]]/span[contains(.,"Логин")]')

    @property
    def password_input(self) -> Locator:
        return self.locator('//label[span[contains(.,"Пароль")]]/div/input')

    @property
    def password_input_title(self) -> Locator:
        return self.locator('//label[@class[contains(.,"Input_Input")]]/span[contains(.,"Пароль")]')

    @property
    def password_input_hidden(self) -> Locator:
        return self.locator('//label[span[contains(.,"Пароль")]]/div/input[@type[contains(., "password")]]')

    @property
    def password_input_visible(self) -> Locator:
        return self.locator('//label[span[contains(.,"Пароль")]]/div/input[@type[contains(., "text")]]')

    @property
    def password_display_button(self) -> Locator:
        return self.locator('//button[@class[contains(.,"IconButton")]]')

    @property
    def submit_button(self) -> Locator:
        return self.locator('//button[span[contains(.,"Войти")]]')

    @property
    def session_request_path(self) -> str:
        return '/api/auth/session'

    @property
    def credentials_request_path(self) -> str:
        return 'api/auth/callback/credentials?'

    @property
    def session_credentials_lambda(self) -> typing.Callable:
        return lambda r: self.credentials_request_path in r.url and r.request.method == 'POST'

    @property
    def session_response_lambda(self) -> typing.Callable:
        return lambda r: self.session_request_path in r.url and r.request.method == 'GET'

    @property
    def logo_container(self) -> Locator:
        return self.locator('div[class*="AuthLayout_LogoContainer"]')

    def check_specific_locators(self) -> None:
        expect(self.page).to_have_title(self.title)
        expect(self.logo).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.login_input).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.password_input).to_be_visible(timeout=Timeouts.DEFAULT)

    def check_form_title_text(self):
        expect(self.form_title_text).to_be_visible()

    def check_form_subtitle_text(self):
        expect(self.form_subtitle_text).to_be_visible()

    def check_login_input_title(self):
        expect(self.login_input_title).to_be_visible()

    def check_password_input_title(self):
        expect(self.password_input_title).to_be_visible()

    def check_submit_button_text(self):
        expect(self.submit_button).to_be_visible()

    def check_disabled_submit_button(self):
        expect(self.submit_button).to_be_disabled()

    def check_enabled_submit_button(self):
        expect(self.submit_button).to_be_enabled()

    def check_login_input_value(self, login: str):
        expect(self.login_input).to_have_value(login)

    def check_password_input_value_hidden(self, password: str):
        expect(self.password_input).to_have_value(password)
        expect(self.password_input_hidden).to_be_visible()

    def check_password_input_value_visible(self, password: str):
        expect(self.password_input).to_have_value(password)
        expect(self.password_input_visible).to_be_visible()
