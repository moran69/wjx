import time
import logging
from app.bot import TelegramBot
from app.fetcher import fetch_question_data
from app.analyzer import analyze_survey_data
from app.utils import get_beijing_time
from config.settings import *
def monitor_survey():
    """主监控函数"""
    # 初始化Telegram机器人
    bot = TelegramBot(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
    url = os.getenv("QUESTIONNAIRE_URL")
    
    try:
        while True:
            current_time = get_beijing_time()
            
            # 发送开始获取数据的通知
            start_message = f"🔄 正在获取 {current_time} 的问卷数据..."
            bot.send_message(start_message)
            
            # 1. 获取问卷数据
            survey_data = fetch_question_data(url)
            if not survey_data:
                error_message = f"{current_time} ❌ 获取问卷数据失败"
                bot.send_message(error_message)
                time.sleep(300)  # 5分钟
                continue
            
            # 发送数据获取成功的通知
            success_message = f"✅ {current_time} 的实时数据获取成功\n📝 正在调用AI形成简短报告..."
            bot.send_message(success_message)
            
            # 2. 保存数据到JSON
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'survey_data_{timestamp}.json'
            saved_file = save_to_json(survey_data, filename)
            
            if not saved_file:
                error_message = f"{current_time} ❌ 保存数据失败"
                bot.send_message(error_message)
                time.sleep(300)
                continue
            
            # 3. 分析数据
            # 首先尝试使用默认模型
            analysis = analyze_survey_data(saved_file)
            
            if not analysis:
                error_message = f"{current_time} ⚠️ 数据暂时解析失败\n\n尝试其他ai模型\n"
                bot.send_message(error_message)
                
                # 尝试其他模型
                models=["gpt-4o","gpt-4-turbo","gpt-4o-mini","gpt-4o-2024-11-20","gpt-3.5-turbo-16k","gpt-3.5-turbo","airoboros-70b","athene-v2-chat","blackboxai","blackboxai-pro","c4ai-aya-expanse-32b","claude-3-5-sonnet-20240620","claude-3-5-sonnet-20241022","claude-3-haiku","claude-3-haiku-20240307","claude-3-opus-20240229","claude-3-sonnet-20240229","codeqwen1.5-7b-chat","codestral-2405","command-r","command-r-08-2024","command-r-plus","command-r-plus-08-2024","command-r7b","dall-e-3","dbrx-instruct","deepseek-chat","deepseek-r1","deepseek-r1-distill-llama-70b","deepseek-r1-distill-qwen-32b","deepseek-reasoner","deepseek-v2.5","deepseek-v3","distil-whisper-large-v3-en","dolphin-2.6","dolphin-2.9","eureka-chatbot","evil","f1-mini-preview","flux","flux-dev","flux-pro","flux-schnell","gemini","gemini-1.5-flash","gemini-1.5-flash-001","gemini-1.5-flash-002","gemini-1.5-flash-8b-001","gemini-1.5-pro","gemini-1.5-pro-001","gemini-1.5-pro-002","gemini-2.0-flash","gemini-2.0-flash-thinking","gemini-exp","gemini-exp-1114","gemini-exp-1121","gemma-2-27b-it","gemma-2-2b-it","gemma-2-9b-it","gemma2-9b-it","GigaChat:latest","glm-4","glm-4-plus","gpt-3.5-turbo-0125","gpt-4","gpt-4o","gpt-4o-2024-05-13","gpt-4o-2024-08-06","gpt-4o-mini","gpt-4o-mini-2024-07-18","grok-2-2024-08-13","grok-2-mini-2024-08-13","hermes-2-dpo","hunyuan-standard-256k","im-a-good-gpt2-chatbot","im-also-a-good-gpt2-chatbot","jamba-1.5-large","jamba-1.5-mini","Janus_Pro_7B","llama-2-7b","llama-3-70b","llama-3-70b-instruct","llama-3-8b","llama-3-8b-instruct","llama-3.1-405b","llama-3.1-405b-instruct-bf16","llama-3.1-405b-instruct-fp8","llama-3.1-70b","llama-3.1-70b-instruct","llama-3.1-8b","llama-3.1-8b-instant","llama-3.1-8b-instruct","llama-3.1-nemotron-51b-instruct","llama-3.1-nemotron-70b-instruct","llama-3.2-11b","llama-3.2-11b-vision-preview","llama-3.2-1b","llama-3.2-1b-instruct","llama-3.2-1b-preview","llama-3.2-3b","llama-3.2-3b-instruct","llama-3.2-3b-preview","llama-3.2-90b","llama-3.2-90b-vision-preview","llama-3.2-vision-11b-instruct","llama-3.2-vision-90b-instruct","llama-3.3-70b","llama-3.3-70b-specdec","llama-3.3-70b-versatile","llama-guard-3-8b","llama3-70b-8192","llama3-8b-8192","lzlv-70b","meta-ai","midjourney","minicpm-2.5","MiniMax","ministral-8b-2410","mistral-large-2407","mistral-large-2411","mistral-nemo","mixtral-8x22b","mixtral-8x22b-instruct-v0.1","mixtral-8x7b","mixtral-8x7b-32768","mixtral-8x7b-instruct-v0.1","mixtral-small-28b","molmo-72b-0924","molmo-7b-d-0924","nemotron-4-340b","nemotron-70b","o1","o1-mini","o1-preview","o3-mini","phi-3-mini-4k-instruct-june-2024","phi-3.5-mini","phi-4","pi","pixtral-12b-2409","pixtral-large-2411","qvq-72b","Qwen_QVQ_72B","Qwen_Qwen_2_72B_Instruct","qwen-1.5-7b","qwen-1.8b-chat","qwen-1.8b-longcontext-chat","qwen-14b-chat","qwen-2-72b","qwen-2-vl-7b","qwen-2.5-1m-demo","qwen-2.5-32b","qwen-2.5-72b","qwen-2.5-coder-32b","qwen-72b-chat","qwen-7b-chat","qwen-coder-plus","qwen-coder-plus-1106","qwen-coder-plus-latest","qwen-coder-turbo","qwen-coder-turbo-0919","qwen-coder-turbo-latest","qwen-long","qwen-math-plus","qwen-math-plus-0919","qwen-math-plus-latest","qwen-math-turbo","qwen-math-turbo-0919","qwen-math-turbo-latest","qwen-max","qwen-max-0107","qwen-max-0403","qwen-max-0428","qwen-max-0919","qwen-max-1201","qwen-max-latest","qwen-max-longcontext","qwen-plus","qwen-plus-0828","qwen-plus-0919","qwen-plus-latest","qwen-turbo","qwen-turbo-0919","qwen-turbo-latest","qwen-vl-max","qwen-vl-max-0809","qwen-vl-ocr","qwen-vl-ocr-latest","qwen-vl-plus","qwen1.5-0.5b-chat","qwen1.5-1.8b-chat","qwen1.5-110b-chat","qwen1.5-14b-chat","qwen1.5-32b-chat","qwen1.5-72b-chat","qwen1.5-7b-chat","qwen2-0.5b-instruct","qwen2-1.5b-instruct","qwen2-57b-a14b-instruct","qwen2-72b-instruct","qwen2-7b-instruct","qwen2.5-0.5b-instruct","qwen2.5-1.5b-instruct","qwen2.5-14b-instruct","qwen2.5-32b-instruct","qwen2.5-3b-instruct","qwen2.5-72b-instruct","qwen2.5-7b-instruct","qwen2.5-coder-0.5b-instruct","qwen2.5-coder-14b-instruct","qwen2.5-coder-32b-instruct","qwen2.5-coder-3b-instruct","qwen2.5-coder-7b-instruct","qwen2.5-math-1.5b-instruct","qwen2.5-math-72b-instruct","qwen2.5-math-7b-instruct","qwq-32b","reka-core","reka-core-20240904","reka-flash-20240904","sd-3.5","sdxl-turbo","sonar","sonar-pro","sonar-reasoning","sonar-reasoning-pro","whisper-large-v3","whisper-large-v3-turbo","wizardlm-2-7b","wizardlm-2-8x22b","yi-34b","yi-lightning","yi-vision"]
                
                for fallback_model in models:
                    try:
                        logging.info(f"尝试使用备选模型: {fallback_model}")
                        retry_message = f"{current_time} 🔄 正在尝试使用 {fallback_model} 重新分析..."
                        bot.send_message(retry_message)
                        
                        # 尝试使用当前模型分析
                        analysis = analyze_survey_data(saved_file, fallback_model)
                        
                        if analysis:
                            message = f"📊 问卷分析报告 ({current_time})\n使用模型: {fallback_model}\n\n{analysis}"
                            bot.send_message(message)
                            break
                        else:
                            # 如果分析失败，发送失败消息
                            fail_message = f"❌ {fallback_model} 分析失败，10秒后尝试下一个模型..."
                            bot.send_message(fail_message)
                            
                        # 等待10秒后尝试下一个模型
                        time.sleep(10)
                        
                    except Exception as e:
                        error_message = f"⚠️ {fallback_model} 出现错误: {str(e)}"
                        logging.error(error_message)
                        bot.send_message(error_message)
                        time.sleep(10)  # 发生错误也等待10秒
                        continue
                
                if not analysis:
                    final_error = f"{current_time} ❌ 所有模型分析均失败"
                    bot.send_message(final_error)
            else:
                # 原始分析成功
                message = f"📊 问卷分析报告 ({current_time})\n使用模型: gpt-4o\n\n{analysis}"
                bot.send_message(message)
            
            # 定时30分钟，循环运行
            time.sleep(1800)
            
    except KeyboardInterrupt:
        stop_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 🛑 监控已停止"
        bot.send_message(stop_message)
        logging.info(stop_message)
    except Exception as e:
        error_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ❌ 程序发生严重错误: {e}"
        bot.send_message(error_message)
        logging.critical(error_message)

if __name__ == "__main__":
    monitor_survey()
