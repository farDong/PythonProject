"""
工具类：日志工具、JSON 测试数据读取工具、Allure 报告辅助。
"""
import json
import logging
import os
import time

import config


# ================= 日志工具 =================
class Logger:
    """项目统一日志：同时输出到控制台和 log/ 目录下的文件。"""

    _logger = None

    @classmethod
    def get_logger(cls, name="ui-test"):
        if cls._logger is not None:
            return cls._logger

        os.makedirs(config.LOG_DIR, exist_ok=True)
        log_file = os.path.join(
            config.LOG_DIR, time.strftime("%Y%m%d_%H%M%S") + ".log"
        )

        logger = logging.getLogger(name)
        logger.setLevel(config.LOG_LEVEL)
        formatter = logging.Formatter(config.LOG_FORMAT, datefmt=config.DATE_FORMAT)

        # 控制台
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        # 文件
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        cls._logger = logger
        return logger


logger = Logger.get_logger()


# ================= 数据工具 =================
class DataTool:
    """读取 data/ 目录下的 JSON 测试数据文件。"""

    @staticmethod
    def load_json(filename):
        """
        读取 JSON 数据文件，返回 Python 对象。
        :param filename: 文件名（如 "login_data.json"），相对 data/ 目录
        """
        filepath = os.path.join(config.DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            logger.info("加载测试数据文件: %s", filepath)
            return json.load(f)


# ================= 报告辅助 =================
class ReportTool:
    """Allure 报告相关辅助方法。"""

    @staticmethod
    def generate_html():
        """
        将 pytest 运行产生的 allure 原始结果渲染为 HTML 报告。
        需要本机已安装 Allure 命令行（allure 命令可用）。
        原始结果目录: report/allure-results
        输出目录:     report/allure-html
        """
        result_dir = os.path.join(config.ALLURE_RESULT_DIR, "allure-results")
        html_dir = os.path.join(config.ALLURE_RESULT_DIR, "allure-html")
        cmd = f'allure generate "{result_dir}" -o "{html_dir}" --clean'
        ret = os.system(cmd)
        if ret == 0:
            logger.info("Allure HTML 报告已生成: %s", html_dir)
            os.system(f'allure open "{html_dir}"')
        else:
            logger.error(
                "生成 Allure 报告失败，请确认已安装 Allure 命令行工具"
                "（https://github.com/allure-framework/allure2）"
            )
