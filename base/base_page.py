"""
所有页面公共操作方法（BasePage）
统一使用显式等待（WebDriverWait + expected_conditions）封装，
页面子类只关心元素定位和业务动作。
"""
import os
import time

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import config
from tool import logger


class BasePage:
    """页面基类：封装显式等待和常用页面操作。"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, config.EXPLICIT_TIMEOUT, poll_frequency=config.POLL_FREQUENCY
        )

    # ================= 元素等待与获取 =================
    def find(self, locator: tuple[By, str], timeout: int = None) -> WebElement:
        """显式等待元素可见并返回该元素。"""
        wait = self._wait_with_timeout(timeout)
        logger.debug("等待元素可见: %s", locator)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: tuple[By, str], timeout: int = None) -> list[WebElement]:
        """显式等待一组元素存在并返回元素列表。"""
        wait = self._wait_with_timeout(timeout)
        logger.debug("等待元素列表出现: %s", locator)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def _wait_with_timeout(self, timeout: int) -> WebDriverWait:
        """临时覆盖超时时间（如某些加载很慢的元素）。"""
        if timeout is None:
            return self.wait
        return WebDriverWait(
            self.driver, timeout, poll_frequency=config.POLL_FREQUENCY
        )

    def wait_clickable(self, locator: tuple[By, str], timeout: int = None) -> WebElement:
        """显式等待元素可点击并返回该元素。"""
        wait = self._wait_with_timeout(timeout)
        logger.debug("等待元素可点击: %s", locator)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator: tuple[By, str], timeout: int = None) -> bool:
        """显式等待元素不可见/消失。"""
        wait = self._wait_with_timeout(timeout)
        logger.debug("等待元素消失: %s", locator)
        return wait.until(EC.invisibility_of_element_located(locator))

    def is_element_present(self, locator: tuple[By, str], timeout: int = None) -> bool:
        """判断元素是否出现（不抛异常，用于断言）。"""
        try:
            self._wait_with_timeout(timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ================= 基础操作 =================
    def open(self, url: str = None):
        """打开网页。"""
        target = url or config.URL
        logger.info("打开网页: %s", target)
        self.driver.get(target)
        return self

    def click(self, locator: tuple[By, str], timeout: int = None):
        """显式等待元素可点击后点击。"""
        element = self.wait_clickable(locator, timeout)
        logger.info("点击元素: %s", locator)
        element.click()
        return self

    def js_click(self, locator: tuple[By, str], timeout: int = None):
        """通过 JS 点击（用于普通 click 被遮挡时）。"""
        element = self.wait_clickable(locator, timeout)
        logger.info("JS 点击元素: %s", locator)
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def input_text(self, locator: tuple[By, str], text: str, timeout: int = None):
        """先清空再输入文本。"""
        element = self.find(locator, timeout)
        logger.info("输入文本 %r -> %s", text, locator)
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator: tuple[By, str], timeout: int = None) -> str:
        """获取元素文本。"""
        text = self.find(locator, timeout).text
        logger.info("获取元素文本 %r <- %s", text, locator)
        return text

    def get_attribute(self, locator: tuple[By, str], attribute: str,
                      timeout: int = None) -> str:
        """获取元素属性值。"""
        value = self.find(locator, timeout).get_attribute(attribute)
        logger.info("获取元素属性 %s=%r <- %s", attribute, value, locator)
        return value

    def get_input_value(self, locator: tuple[By, str], timeout: int = None) -> str:
        """获取输入框的 value。"""
        return self.get_attribute(locator, "value", timeout)

    # ================= 下拉框 =================
    def select_by_text(self, locator: tuple[By, str], text: str):
        """按可见文本选择下拉选项。"""
        logger.info("下拉框按文本选择: %r -> %s", text, locator)
        Select(self.find(locator)).select_by_visible_text(text)
        return self

    def select_by_value(self, locator: tuple[By, str], value: str):
        """按 value 选择下拉选项。"""
        logger.info("下拉框按 value 选择: %r -> %s", value, locator)
        Select(self.find(locator)).select_by_value(value)
        return self

    def select_by_index(self, locator: tuple[By, str], index: int):
        """按索引选择下拉选项。"""
        logger.info("下拉框按索引选择: %d -> %s", index, locator)
        Select(self.find(locator)).select_by_index(index)
        return self

    # ================= 鼠标 / 键盘 / 滚动 =================
    def hover(self, locator: tuple[By, str]):
        """鼠标悬停在元素上。"""
        element = self.find(locator)
        logger.info("鼠标悬停: %s", locator)
        ActionChains(self.driver).move_to_element(element).perform()
        return self

    def double_click(self, locator: tuple[By, str]):
        """双击元素。"""
        element = self.wait_clickable(locator)
        logger.info("双击元素: %s", locator)
        ActionChains(self.driver).double_click(element).perform()
        return self

    def scroll_to_element(self, locator: tuple[By, str]):
        """滚动到元素可见。"""
        element = self.find(locator)
        logger.info("滚动到元素: %s", locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return self

    def scroll_to_bottom(self):
        """滚动到页面底部。"""
        logger.info("滚动到页面底部")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self

    # ================= 窗口 / iframe / alert =================
    def switch_to_window_by_title(self, title: str, timeout: int = None):
        """切换到指定标题的窗口。"""
        wait = self._wait_with_timeout(timeout)

        def _switch(driver):
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if driver.title == title:
                    return True
            return False

        logger.info("切换到标题为 %r 的窗口", title)
        wait.until(_switch)
        return self

    def switch_to_frame(self, locator: tuple[By, str], timeout: int = None):
        """切换进 iframe。"""
        wait = self._wait_with_timeout(timeout)
        logger.info("切换进 iframe: %s", locator)
        wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
        return self

    def switch_to_default_content(self):
        """退出 iframe，回到主文档。"""
        logger.info("退出 iframe 回到主文档")
        self.driver.switch_to.default_content()
        return self

    def accept_alert(self, timeout: int = None):
        """等待 alert 出现并点击确定。"""
        wait = self._wait_with_timeout(timeout)
        logger.info("等待 alert 并接受")
        wait.until(EC.alert_is_present()).accept()
        return self

    def dismiss_alert(self, timeout: int = None):
        """等待 alert 出现并点击取消。"""
        wait = self._wait_with_timeout(timeout)
        logger.info("等待 alert 并取消")
        wait.until(EC.alert_is_present()).dismiss()
        return self

    # ================= 截图 =================
    def take_screenshot(self, name: str = None) -> str | None:
        """截图并保存到 report/screenshots/ 目录，返回文件路径。"""
        try:
            os_dir = config.SCREENSHOT_DIR
            if not os.path.exists(os_dir):
                os.makedirs(os_dir, exist_ok=True)
            filename = time.strftime("%Y%m%d_%H%M%S") + "_" + (name or "screenshot") + ".png"
            filepath = os.path.join(os_dir, filename)
            self.driver.get_screenshot_as_file(filepath)
            logger.info("截图保存: %s", filepath)
            return filepath
        except UnexpectedAlertPresentException:
            logger.error("存在未处理的 alert，截图失败")
        except Exception as e:
            logger.error("截图失败: %s", e)
        return None

    # ================= 其它 =================
    def get_page_title(self) -> str:
        """获取当前页面标题。"""
        return self.driver.title

    def get_current_url(self) -> str:
        """获取当前页面 URL。"""
        return self.driver.current_url

    def refresh(self):
        """刷新页面。"""
        logger.info("刷新页面")
        self.driver.refresh()
        return self

    def back(self):
        """浏览器后退。"""
        logger.info("浏览器后退")
        self.driver.back()
        return self

    def forward(self):
        """浏览器前进。"""
        logger.info("浏览器前进")
        self.driver.forward()
        return self
