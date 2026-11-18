"""
页面对象：登录页
定位器集中定义为类属性，后续可直接修改/添加。
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from tool import logger


class LoginPage(BasePage):
    """https://www.saucedemo.com 登录页"""

    # ---------------- 元素定位 ----------------
    USERNAME_INPUT = (By.ID, "user-name")           # 用户名输入框
    PASSWORD_INPUT = (By.ID, "password")            # 密码输入框
    LOGIN_BUTTON = (By.ID, "login-button")          # 登录按钮
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")  # 错误提示条
    LOGO = (By.CLASS_NAME, "login_logo")            # 登录页 LOGO

    # ---------------- 页面动作 ----------------
    def open_login_page(self):
        """打开登录页。"""
        logger.info("打开登录页")
        self.open()
        self.find(self.LOGO)  # 显式等待页面加载完成
        return self

    def input_username(self, username: str):
        """输入用户名。"""
        self.input_text(self.USERNAME_INPUT, username)
        return self

    def input_password(self, password: str):
        """输入密码。"""
        self.input_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """点击登录按钮。
        登录失败会停留在登录页并显示错误提示，此时返回 LoginPage 自身；
        登录成功跳转商品页，返回 ProductsPage。"""
        self.click(self.LOGIN_BUTTON)
        if self.is_element_present(self.ERROR_MESSAGE, timeout=3):
            return self
        from page.products_page import ProductsPage
        return ProductsPage(self.driver)

    def login(self, username: str, password: str):
        """完整登录动作：输入账号密码并点击登录。"""
        logger.info("执行登录: username=%s", username)
        self.input_username(username)
        self.input_password(password)
        return self.click_login()

    # ---------------- 断言辅助 ----------------
    def get_error_message(self) -> str:
        """获取登录失败的错误提示文本。"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        """判断当前是否停留在登录页。"""
        return self.is_element_present(self.LOGIN_BUTTON, timeout=3)
