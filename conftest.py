"""
pytest 全局 fixture：
- 会话启动时打开 Edge 浏览器，会话结束时关闭
- 每条用例注入 driver，并在用例失败时自动截图
"""
import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

import config
from tool import logger


@pytest.fixture(scope="session")
def driver():
    """session 级浏览器 fixture：整个测试会话共用一个 Edge 实例。"""
    logger.info("启动 %s 浏览器", config.BROWSER)

    options = EdgeOptions()
    if config.BROWSER == "headless_edge":
        options.add_argument("--headless=new")

    # Selenium 4.6+ 自带 Selenium Manager，会自动下载匹配的 EdgeDriver
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

    yield driver

    logger.info("关闭浏览器")
    driver.quit()


@pytest.fixture(scope="function")
def case_driver(request, driver):
    """函数级 fixture：记录用例开始/结束，失败时自动截图并附加到 Allure。"""
    import allure
    import os
    import time

    case_name = request.node.name
    logger.info("========== 用例开始: %s ==========", case_name)

    yield driver

    # 失败自动截图（结果由 pytest_runtest_makereport 钩子挂到 item 上）
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        filename = time.strftime("%Y%m%d_%H%M%S") + "_" + case_name + ".png"
        os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
        filepath = os.path.join(config.SCREENSHOT_DIR, filename)
        driver.get_screenshot_as_file(filepath)
        logger.error("用例失败，已截图: %s", filepath)
        # 同时把截图附到 allure 报告里
        with open(filepath, "rb") as f:
            allure.attach(
                f.read(),
                name=case_name + "_failure",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """把每条用例的执行结果挂到 item 上，供失败截图使用。"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
