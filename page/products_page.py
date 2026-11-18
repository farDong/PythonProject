"""
页面对象：商品页（登录成功后的首页）
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from tool import logger


class ProductsPage(BasePage):
    """https://www.saucedemo.com/inventory.html 商品列表页"""

    # ---------------- 元素定位 ----------------
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")                       # 页面标题 "Products"
    INVENTORY_LIST = (By.ID, "inventory_container")                 # 商品列表容器
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")             # 所有商品条目
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")             # 商品名称列表
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory") # 所有"加入购物车"按钮
    SHOPPING_CART_LINK = (By.ID, "shopping_cart_container")         # 购物车入口
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")             # 购物车数量角标
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")                  # 左上角菜单
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")                    # 退出登录

    # ---------------- 页面动作 ----------------
    def is_products_page(self) -> bool:
        """判断是否进入商品页。"""
        return self.is_element_present(self.INVENTORY_LIST, timeout=5)

    def get_products_title(self) -> str:
        """获取页面标题文本（应为 'Products'）。"""
        return self.get_text(self.PRODUCTS_TITLE)

    def get_item_names(self) -> list[str]:
        """获取所有商品名称。"""
        items = self.find_all(self.ITEM_NAMES)
        names = [item.text for item in items]
        logger.info("获取到 %d 个商品: %s", len(names), names)
        return names

    def add_first_item_to_cart(self):
        """把第一个商品加入购物车。"""
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        logger.info("把第一个商品加入购物车")
        buttons[0].click()
        return self

    def get_cart_count(self) -> int:
        """获取购物车角标数量，购物车为空时返回 0。"""
        if not self.is_element_present(self.CART_BADGE, timeout=2):
            logger.info("购物车为空")
            return 0
        return int(self.get_text(self.CART_BADGE))

    def go_to_cart(self):
        """进入购物车页。"""
        self.click(self.SHOPPING_CART_LINK)
        return self

    def logout(self):
        """打开左侧菜单并退出登录，回到登录页。"""
        logger.info("退出登录")
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        from page.login_page import LoginPage
        return LoginPage(self.driver)
