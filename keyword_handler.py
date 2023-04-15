from config import keyword_list_paths, keyword_length_limit
import random
import logging

logging.basicConfig(level=logging.DEBUG)
class KyHandler:
    keywords_path = None
    keywords = None
    length_limit = 0
    keywords_all = []
    keywords = []

    def __init__(self):
        self.get_random_key_path()
        self.length_limit = keyword_length_limit
        self.set_keywords()

    def get_random_key_path(self):
        while True:
            random_key = random.choice(list(keyword_list_paths.keys()))
            self.keywords_path = keyword_list_paths.get(random_key)
            if self.keywords_path:
                break

    def get_random_list(self, len_list=1):
        result = {}
        while True:
            if len(result) >= self.length_limit:
                return list(result.keys())

            index_ = random.randint(0, len_list)
            if result.get(index_, None):
                continue
            else:
                result[index_] = index_

    def load_keyword(self):
        with open(self.keywords_path, 'r', encoding='utf-8') as fk:
            self.keywords_all = fk.readlines()
            fk.close()

    def save_keyword(self):
        with open(self.keywords_path, 'w', encoding='utf-8') as fk:
            fk.write(''.join(self.keywords_all))
            fk.close()

    def set_keywords(self):
        self.load_keyword()
        if not self.keywords_all:
            logging.error('failed load keyword list')

        indexes = self.get_random_list(len(self.keywords_all))

        for index in indexes:
            keyword = self.keywords_all.pop(index)
            self.keywords.append(str(keyword).strip())

        # better call it after operation done!
        # self.save_keyword()
