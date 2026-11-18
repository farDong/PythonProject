# UI 自动化测试框架（Python + Selenium + PO + pytest）

测试对象：https://www.saucedemo.com （Edge 浏览器）

## 目录结构

```
PythonProject1/
├── base/               # 所有页面公共操作方法
│   └── base_page.py    # BasePage：显式等待封装的 find/click/input/下拉/滚动/截图/窗口/alert 等
├── page/               # 页面对象
│   ├── login_page.py   # 登录页
│   └── products_page.py# 商品页
├── data/               # 测试数据（JSON）
│   └── login_data.json
├── log/                # 脚本日志（每次运行自动生成）
├── report/             # 测试报告（运行后自动生成）
│   ├── allure-results/ # pytest 自动输出的 allure 原始结果
│   ├── allure-html/    # allure 渲染后的 HTML 报告
│   └── screenshots/    # 失败自动截图
├── script/             # 测试脚本
│   └── test_login.py
├── config.py           # 项目配置（URL/浏览器/超时/日志等）
├── conftest.py         # pytest fixture：Edge 启动关闭、失败自动截图
├── pytest.ini          # pytest 配置
├── tool.py             # 工具类：日志 Logger、数据 DataTool、报告 ReportTool
└── requirements.txt
```

## 环境准备（PyCharm）

1. Interpreter 选择 Python 3.13（本机 `F:\develop\Python313`）。
2. 终端执行：`pip install -r requirements.txt`
3. Allure 报告渲染需要 Java + Allure 命令行（本机已有 `F:\OtherTools\allure-2.46.2` 和 JDK17，
   确保环境变量里 `JAVA_HOME=F:\develop\Java\JDK-17`，并把 `F:\OtherTools\allure-2.46.2\bin` 加入 PATH）。

## 运行用例

```bash
# 运行全部用例（pytest.ini 已配置 --alluredir，自动产生报告数据）
pytest

# 只跑登录模块
pytest script/test_login.py
```

运行后自动产出：`log/` 日志、`report/allure-results/` 结果、失败用例截图。

## 查看 Allure 报告

```bash
# 方式一：生成静态 HTML 后用浏览器打开 report/allure-html/index.html
allure generate report/allure-results -o report/allure-html --clean

# 方式二：直接起本地服务在线看
allure serve report/allure-results
```

也可以在 Python 里调用：`python -c "from tool import ReportTool; ReportTool.generate_html()"`

## 如何扩展

- **加页面**：在 `page/` 新建 `xxx_page.py`，继承 `base.base_page.BasePage`，定位器写成类属性。
- **加公共方法**：优先加到 `base/base_page.py`，所有页面共享。
- **加数据**：在 `data/` 建 JSON 文件，用 `from tool import DataTool; DataTool.load_json("xxx.json")` 读取。
- **加用例**：在 `script/` 新建 `test_xxx.py`，方法参数传 `case_driver`，用 `allure.step()` 描述步骤。
- **改环境**：只改 `config.py`（URL、浏览器、超时等）。
