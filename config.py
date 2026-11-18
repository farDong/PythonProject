"""
项目配置文件
集中管理环境、浏览器、超时、日志等配置项，方便统一修改。
"""
import os

# 项目根目录（config.py 所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- 环境配置 ----------------
# 测试网站地址
URL = "https://www.saucedemo.com"

# 浏览器类型：edge / chrome / firefox
BROWSER = "edge"

# ---------------- 超时配置（秒） ----------------
# 显式等待默认超时时间
EXPLICIT_TIMEOUT = 10
# 轮询间隔
POLL_FREQUENCY = 0.5
# 页面加载超时
PAGE_LOAD_TIMEOUT = 30

# ---------------- 截图配置 ----------------
# 失败截图保存目录
SCREENSHOT_DIR = os.path.join(BASE_DIR, "report", "screenshots")

# ---------------- 日志配置 ----------------
# 日志存放目录
LOG_DIR = os.path.join(BASE_DIR, "log")
# 日志级别：DEBUG / INFO / WARNING / ERROR
LOG_LEVEL = "INFO"
# 日志文件名格式
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
# 控制台/文件日期格式
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ---------------- 测试数据配置 ----------------
# 数据目录
DATA_DIR = os.path.join(BASE_DIR, "data")

# ---------------- 报告配置 ----------------
# pytest 运行后 allure 原始结果目录
ALLURE_RESULT_DIR = os.path.join(BASE_DIR, "report")
