import json
import requests
import logging

API_KEY = "sk-fyKEGKfwJcoOwb8fYnY"

def analyze_survey_data(json_file_path, model="gpt-4o-mini"):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            survey_data = json.load(f)
        
        api_url = "https://api-1-hemf.onrender.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        prompt = "请对以下调查结果进行一段话总结:\n\n" + json.dumps(survey_data, ensure_ascii=False, indent=2)
        
        data = {
            "model": model,
            "messages": [{"role": "system", "content": "你是一个专业的数据分析师"}, {"role": "user", "content": prompt}]
        }
        
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            logging.error(f"API request failed: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error analyzing data: {e}")
        return None
