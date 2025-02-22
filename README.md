# wjx
实时跟踪问卷星所发放问卷的数据，并调用ai智能总结当前结果
问卷星数据获取题目+选项情况，保存json文件
![image](https://github.com/user-attachments/assets/b8778c68-9f75-4a1b-a3a9-233b0b1c518a)

![image](https://github.com/user-attachments/assets/e53e9c8b-c290-463b-989d-456fdf2138db)

# 问卷监控工具

## 项目简介

本项目是一个用于监控和分析问卷星问卷数据的工具。它定期从问卷星平台获取数据，保存为 JSON 文件，使用 AI 模型进行分析，并通过 Telegram 发送分析报告。

## 特性

- **定期获取问卷数据**：自动从指定的问卷 URL 获取最新数据。
- **保存数据**：将获取的数据保存为 JSON 文件，方便后续处理。
- **数据分析**：使用 AI 模型对问卷数据进行分析，生成报告。
- **Telegram 通知**：通过 Telegram 发送分析报告和通知。

## 安装与配置

1. **克隆仓库**：

    ```bash
    git clone https://github.com/moran69/wjx.git
    ```


2. **安装依赖**：

    ```bash
    cd wjx
    pip install -r requirements.txt
    ```


3. **配置文件**：

    在 `config/settings.py` 中配置以下信息：  

    - **Telegram Bot Token**： 在 [BotFather](https://core.telegram.org/bots#botfather) 创建一个新的 Telegram 机器人，并获取 Token。  
    - **Telegram Chat ID**： 获取您的 [Telegram Chat ID](https://telegramcnweb.com/post/telegram%E5%A6%82%E4%BD%95%E8%8E%B7%E5%8F%96chat-id/)。  
    - **问卷 URL**： 设置您要监控的问卷的 URL。  

    示例配置：  

    ```python
    TELEGRAM_BOT_TOKEN = '965940462:AAF4VHCv3Fyg04zA32***************'
    TELEGRAM_CHAT_ID = '-1002451041509'
    QUESTIONNAIRE_URL = 'https://www.wjx.cn/report/302104735.aspx?njjc=1'
    ```


## 使用方法

运行主程序开始监控问卷数据：

```bash
python main.py

程序将每隔 30 分钟获取一次问卷数据，进行分析，并通过 Telegram 发送分析报告

 ```
# **贡献**
欢迎提交问题和拉取请求。请在提交前阅读 贡献指南。
感谢[神墨大佬](https://linux.do/u/smnet/summary)提供的公益API服务

# **许可证**
本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。

# **致谢**
感谢以下项目和库的支持：

requests：用于发送 HTTP 请求。
BeautifulSoup：用于解析 HTML 数据。
python-telegram-bot：用于与 Telegram 机器人交互。
pytz：用于处理时区。
