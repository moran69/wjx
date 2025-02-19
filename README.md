# wjx
实时跟踪问卷星所方法问卷的数据，并调用ai智能总结当前结果

# 问卷监控工具

## 项目描述

这是一个问卷监控与分析工具，定期从问卷星平台获取数据，保存数据并使用AI模型进行分析，并通过Telegram发送分析报告。

## 功能

- 定期获取问卷数据。
- 将数据保存为JSON文件。
- 使用AI分析数据。
- 通过Telegram发送通知和分析报告。

## 配置与安装

1. 克隆此仓库。
2. 使用 `pip install -r requirements.txt` 安装依赖。
3. 在 `config/settings.py` 文件中配置您的Telegram Bot Token 和问卷URL。
4. 运行 `main.py` 开始监控问卷数据。

## 使用方法

```bash
python main.py

