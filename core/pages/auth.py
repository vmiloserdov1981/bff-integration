from playwright.sync_api import Page, Locator, expect
import typing


from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class AuthPage(BasePage):

    PATH = 'auth/signin'

    def __init__(self, page: Page, host: str):
        super().__init__(page=page, url=f'http://{host}/{self.PATH}')
        self.title: str = 'Smart Diagnostics'
    
    @property
    def logo(self) -> Locator:
        return self.locator('div[class*="AuthLayout_LogoContainer"]>span[class*="Icon_icon"]>svg')

    @property
    def login_form_title(self) -> Locator:
        return self.locator('//div[@class[contains(.,"SignInForm_Header")]]/span[contains(.,"Войдите в свой аккаунт")]')

    @property
    def login_input(self) -> Locator:
        return self.locator('//label[span[contains(.,"Логин")]]/div/input')

    @property
    def password_input(self) -> Locator:
        return self.locator('//label[span[contains(.,"Пароль")]]/div/input')

    @property
    def submit_button(self) -> Locator:
        return self.locator('//button[span[contains(.,"Войти")]]')

    @property
    def session_request_url(self) -> str:
        return '/api/auth/session'

    @property
    def session_response_lambda(self) -> typing.Callable:
        return lambda r: self.session_request_url in r.url and r.request.method == 'GET'

    def check_specific_locators(self) -> None:
        expect(self.page).to_have_title(self.title)
        expect(self.logo).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.login_input).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.password_input).to_be_visible(timeout=Timeouts.DEFAULT)
