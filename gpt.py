import openai
import time
from config import gpt_token, gpt_execute_limit, gpt_messages_init, gpt_model_tuning
import json
from pathlib import Path


class GPT:
    contens = {}
    command = ''
    response_format = 'put result on json object with tittle on tittle attribut, content on content attribut as html content, and if there any keyword list generated, put it on keywords attribut'
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
        self.command = 'create a chinese article about {}, minimum 1500 character and maximum 2000 character don\'t forget to extract 5 keywords, with rule {}'.format(keyword, self.response_format)
   
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
        chats = self.open_ai.ChatCompletion.create(model=self.model, messages=self.messages)

        self.parsing_to_dict(chats.choices[0].message.content)

    def parsing_to_dict(self, content):
        content_dict = json.loads(content)

        self.contents.append(content_dict)


# if __name__ == "__main__":
#     gpt = GPT()
#     gpt.execute('nodejs tips and trick')
#     gpt.get_images('nodejs tips and trick')
