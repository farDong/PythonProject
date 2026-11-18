"""
登录功能测试用例（示例）
数据来源：data/login_data.json
"""
import allure
import pytest

from page.login_page import LoginPage
from tool import DataTool

# 加载测试数据
LOGIN_DATA = DataTool.load_json("login_data.json")


@allure.epic("SauceDemo 商城")
@allure.feature("登录模块")
class TestLogin:
    """登录页测试。"""

    @allure.story("合法账号登录")
    @allure.title("标准用户登录成功，进入商品页")
    def test_login_success(self, case_driver):
        login_page = LoginPage(case_driver)
        with allure.step("打开登录页"):
            login_page.open_login_page()
        with allure.step("输入标准账号并登录"):
            products_page = login_page.login(
                LOGIN_DATA["valid"]["username"], LOGIN_DATA["valid"]["password"]
            )
        with allure.step("断言进入商品页且标题为 Products"):
            assert products_page.is_products_page(), "登录成功后应进入商品页"
            assert (
                products_page.get_products_title()
                == LOGIN_DATA["products_title"]
            )

    @allure.story("非法登录")
    @allure.title("错误密码登录失败，提示账号密码不匹配")
    def test_login_wrong_password(self, case_driver):
        login_page = LoginPage(case_driver)
        with allure.step("打开登录页"):
            login_page.open_login_page()
        with allure.step("输入错误密码并登录"):
            page = login_page.login(
                LOGIN_DATA["invalid_password"]["username"],
                LOGIN_DATA["invalid_password"]["password"],
            )
        with allure.step("断言仍停留在登录页且提示正确"):
            assert page.is_login_page(), "登录失败应停留在登录页"
            assert page.get_error_message() == LOGIN_DATA["expected_messages"]["invalid_credentials"]

    @allure.story("非法登录")
    @allure.title("用户名为空登录失败，提示用户名必填")
    def test_login_empty_username(self, case_driver):
        login_page = LoginPage(case_driver)
        with allure.step("打开登录页"):
            login_page.open_login_page()
        with allure.step("用户名留空并登录"):
            page = login_page.login(
                LOGIN_DATA["empty_username"]["username"],
                LOGIN_DATA["empty_username"]["password"],
            )
        with allure.step("断言错误提示"):
            assert page.get_error_message() == LOGIN_DATA["expected_messages"]["empty_username"]

    @allure.story("非法登录")
    @allure.title("密码为空登录失败，提示密码必填")
    def test_login_empty_password(self, case_driver):
        login_page = LoginPage(case_driver)
        with allure.step("打开登录页"):
            login_page.open_login_page()
        with allure.step("密码留空并登录"):
            page = login_page.login(
                LOGIN_DATA["empty_password"]["username"],
                LOGIN_DATA["empty_password"]["password"],
            )
        with allure.step("断言错误提示"):
            assert page.get_error_message() == LOGIN_DATA["expected_messages"]["empty_password"]

    @allure.story("非法登录")
    @allure.title("被锁定用户登录失败，提示用户已锁定")
    def test_login_locked_user(self, case_driver):
        login_page = LoginPage(case_driver)
        with allure.step("打开登录页"):
            login_page.open_login_page()
        with allure.step("输入被锁定用户并登录"):
            page = login_page.login(
                LOGIN_DATA["locked_user"]["username"],
                LOGIN_DATA["locked_user"]["password"],
            )
        with allure.step("断言错误提示"):
            assert page.get_error_message() == LOGIN_DATA["expected_messages"]["locked_user"]

    @allure.story("商品页冒烟")
    @allure.title("登录后商品页加载，加入购物车角标数量为 1")
    def test_add_to_cart_after_login(self, case_driver):
        login_page = LoginPage(case_driver)
        with allure.step("登录"):
            login_page.open_login_page()
            products_page = login_page.login(
                LOGIN_DATA["valid"]["username"], LOGIN_DATA["valid"]["password"]
            )
        with allure.step("断言商品列表非空"):
            assert len(products_page.get_item_names()) > 0
        with allure.step("加入购物车并断言角标数量"):
            products_page.add_first_item_to_cart()
            assert products_page.get_cart_count() == 1
