"""
Allure 报告生成脚本

作用：
    调用 allure 命令行，把 pytest 运行产生的原始结果（report/allure-results）
    生成本地 HTML 格式报告，输出到项目根目录的 new_report/ 文件夹。

用法：
    python cmd_allure.py            # 生成报告并自动打开
    python cmd_allure.py --no-open  # 只生成报告，不打开浏览器

前提：
    本机已安装 Allure 命令行工具，且 allure 已加入 PATH
    （下载：https://github.com/allure-framework/allure2/releases）
"""
import argparse
import os
import shutil
import subprocess
import sys
import webbrowser

import config
from tool import logger

# 原始结果目录（pytest.ini 中 --alluredir 指定）
RESULT_DIR = os.path.join(config.ALLURE_RESULT_DIR, "allure-results")

# 生成的 HTML 报告目录
REPORT_DIR = os.path.join(config.BASE_DIR, "new_report")


def find_allure() -> str | None:
    """在 PATH 中查找 allure 命令（Windows 下实际为 allure.BAT），返回完整路径。"""
    return shutil.which("allure")


def check_allure() -> str | None:
    """检查 allure 命令行是否可用，可用则返回其路径。"""
    allure = find_allure()
    if not allure:
        return None
    try:
        # 必须传完整路径：Windows 下 CreateProcess 不会自动解析 PATH 中的 .BAT
        subprocess.run(
            [allure, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return allure
    except (FileNotFoundError, OSError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired):
        return None


def generate_report() -> bool:
    """调用 allure generate 生成本地 HTML 报告，成功返回 True。"""
    if not os.path.isdir(RESULT_DIR):
        logger.error("未找到 Allure 原始结果目录: %s，请先运行 pytest 用例", RESULT_DIR)
        return False

    allure = check_allure()
    if not allure:
        logger.error("未检测到 allure 命令，请安装 Allure 并加入 PATH")
        return False

    cmd = [allure, "generate", RESULT_DIR, "-o", REPORT_DIR, "--clean"]
    logger.info("执行命令: %s", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("生成报告失败:\n%s", result.stderr or result.stdout)
        return False

    logger.info("HTML 报告已生成: %s", os.path.join(REPORT_DIR, "index.html"))
    return True


def open_report():
    """用默认浏览器打开生成的 HTML 报告。"""
    index_file = os.path.join(REPORT_DIR, "index.html")
    if os.path.exists(index_file):
        logger.info("打开报告: %s", index_file)
        webbrowser.open("file:///" + index_file.replace("\\", "/"))


def main():
    parser = argparse.ArgumentParser(description="生成 Allure 本地 HTML 报告")
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="只生成报告，不自动打开浏览器",
    )
    args = parser.parse_args()

    if not generate_report():
        sys.exit(1)

    if not args.no_open:
        open_report()


if __name__ == "__main__":
    main()
