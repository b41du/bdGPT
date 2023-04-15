import openai
import time
from config import gpt_token, gpt_execute_limit, gpt_messages_init, gpt_model_tuning
import json
import logging
import time
import re

logging.basicConfig(level=logging.DEBUG)

class GPT:
    command = ''
    response_format = '将结果放在有效的 json 对象上，标题在 ttl 键上，键 ctt 上的内容作为 html 内容，如果有任何关键字生成列表，将其放在键 kyw 上'
    last_exec_time = None
    messages = gpt_messages_init
    model = gpt_model_tuning
    open_ai = openai
    contents = []

    def __init__(self):
        self.last_exec_time = time.time()
        self.api_key = gpt_token
        self.open_ai.api_key = gpt_token

    def generate_command(self, keyword):
        self.command = '创建关于 {} 的文章，最少 1000 个汉字和最多 1300 个汉字也从中提取 2 个关键字，{}'.format(keyword, self.response_format)
    
    def get_clear_response(self, plain_str):
        clean_str = re.search(r"\*\*\*(.*?)\*\*\*", plain_str)
        if clean_str:
            extracted_string = clean_str.group(1)
            return extracted_string

        return plain_str

    def execute(self, keyword):
        diff_time = abs(self.last_exec_time - time.time())

        if diff_time < gpt_execute_limit:
            time.sleep(gpt_execute_limit - diff_time)

        self.generate_command(keyword=keyword)
        self.messages.append(
            {
                'role' : 'user',
                'content' : self.command
            }
        )

        self.last_exec_time = time.time()
        logging.info('asking chat gpt...')

        message = {
            'role': 'user',
            'content': 'Create me chinese article title about {} with format ***title***'.format(keyword)
        }

        chats = self.open_ai.ChatCompletion.create(model=self.model, messages=[message])
        response_title = chats.choices[0].message.content

        title_clean = self.get_clear_response(response_title)

        message1 = {
            'role': 'user',
            'content': 'Create me chinese article for this title  \"{}\" give me result as html content with maximum length of content 1200 chinese character'.format(title_clean)
        }

        logging.info('asking chat gpt for create content...')
        chats = self.open_ai.ChatCompletion.create(model=self.model, messages=[message1])
        content = chats.choices[0].message.content

        content_dict = {
            'title': title_clean,
            'content': content.strip(),
            'keywords': [keyword]
        }

        self.contents.append(content_dict)

    def generate_image(self, keyword):
        response = self.open_ai.Image.create(
            prompt="{}".format(keyword),
            n=1,
            size="1024x1024"
        )
        link = response['data'][0]['url']
