import requests
import json
from tools.log import info_logger, error_logger, warn_logger


def chat_gpt(redis_client, FromUserName, content, gpt_key):
    new_msg = {"role": "user", "content": content}
    if redis_client.get(FromUserName + '_msg') != 'None' and redis_client.get(FromUserName + '_msg') is not None:
        old_msg = eval(redis_client.get(FromUserName + '_msg'))
        old_msg.append(new_msg)
        messages = old_msg
        redis_client.set(FromUserName + '_msg', str(messages), 1800)
    else:
        messages = [new_msg]
        redis_client.set(FromUserName + '_msg', str(messages), 1800)
    info_logger.info(f'messages提问：{messages}')
    chat_url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", 'Authorization':
        f"Bearer {gpt_key}"}

    data = {"model": "gpt-3.5-turbo", "messages": messages, 'max_tokens': 1024}
    # proxies = {"http": "http://172.20.138.227:7890", "https": "http://172.20.138.227:7890"}
    try:
        _res = requests.post(chat_url, json=data, headers=headers, timeout=120)
        _data = json.loads(_res.text)['choices'][0]['message']['content']
        answer = _data.replace("\n", "")
        info_logger.info(f'回答：{answer}')
        return _data.replace("\n", '')
    except Exception as e:
        error_logger.error(f'chatgpt错误:{e}')
        return '对不起，网络连接失败，请稍后再试'
