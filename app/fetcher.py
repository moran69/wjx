import requests
from bs4 import BeautifulSoup
import logging
import time
import re

def parse_option_data(row):
    try:
        cells = row.find_all('td')
        if len(cells) < 3:
            return None
            
        val_td = cells[0]
        option_value = val_td.get('val', '')
        option_text = val_td.get_text().strip()
        count_td = cells[1]
        count = int(count_td.get_text().strip()) if count_td.get_text().strip().isdigit() else 0
        percent_td = cells[2]
        percent = 0
        if percent_td:
            bar_div = percent_td.find('div', class_='bar')
            if bar_div:
                style = bar_div.find('div').get('style', '')
                percent_match = re.search(r'width:\s*([\d.]+)%', style)
                percent = float(percent_match.group(1)) if percent_match else 0
        return {'option_value': option_value, 'option_text': option_text, 'count': count, 'percent': percent}
    except Exception as e:
        logging.warning(f"Error parsing option data: {e}")
        return None

def fetch_question_data(url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            if response.status_code != 200:
                logging.error(f"Failed to fetch data: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            questions = []
            title_items = soup.find_all('div', class_='title-item')
            for i, item in enumerate(title_items, 1):
                try:
                    title_div = item.find('div', class_='title')
                    if not title_div:
                        continue
                    title = title_div.get_text().strip()
                    table = item.find('table', class_='wjxui-table')
                    options = []
                    if table:
                        rows = table.find_all('tr')
                        for row in rows:
                            if 'style' in row.attrs and 'background:#f5f5f5' in row['style']:
                                continue
                            option_data = parse_option_data(row)
                            if option_data:
                                options.append(option_data)
                    question_data = {'question_number': i, 'title': title, 'options': options, 'total_responses': sum(opt['count'] for opt in options) if options else 0}
                    questions.append(question_data)
                except Exception as e:
                    logging.warning(f"Error processing question: {e}")
                    continue
            if questions:
                return {'survey_data': {'total_questions': len(questions), 'questions': questions}}
            logging.warning("No question data found")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            continue
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            continue
