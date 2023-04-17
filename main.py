from keyword_handler import KyHandler
from img_handler import ImgHandler
from orator import DatabaseManager
from config import db_config
from gpt import GPT
import logging
from article import Article

logging.basicConfig(level=logging.DEBUG)

class Main:
    keywords = None
    GPT = None
    contents = None
    img = None
    db = None
    contents = []

    def __init__(self):
        self.khandler = KyHandler()
        self.keywords = self.khandler.keywords
        self.GPT = GPT()
        self.img = ImgHandler()

    def get_db(self):
        if not self.db:
            self.db = DatabaseManager(db_config)
            logging.info('database initiated...')

            return self.db

        return self.db


    def add_image_to_content(self, image_path, content_dict):
        content_html = '<img src="{}" alt="{}"><br>{}'.format(image_path, content_dict.get('title'), content_dict.get('content'))
        return {
            'title': content_dict['title'],
            'content': content_html,
            'keywords': content_dict['keywords']
        }

    def execute(self):
        for keyword in self.keywords:
            try:
                self.GPT.execute(keyword=keyword)
                logging.info('{} generated'.format(keyword), exc_info=True)

                content = self.GPT.contents[-1] if self.GPT.contents else {}

                if not content or not content.get('title') or not content.get('content'):
                    logging.warning('No content generated from chat gpt')
                    continue
                
                tittle = content.get('title')
                image_path = self.img.generate_images(keyword=tittle)

                if not image_path:
                    logging.error('failed save image...', exc_info=True)
                    continue

                single_content = self.add_image_to_content(
                    image_path=image_path,
                    content_dict=content
                )

                article = Article(
                    cate_id=1,
                    title=single_content['title'],
                    content=single_content['content'],
                    keywords=single_content['keywords'],
                    db=self.get_db()
                )

                self.contents.append(article.get_post_dict())

            except Exception as e:
                logging.error(e, exc_info=True)
                continue

        if self.contents:
            db = self.get_db()
            db.table('zbp_post').insert(
                self.contents
            )
            self.khandler.save_keyword()
        # for content in self.GPT.contens:
        #     pass


if __name__ == "__main__":
    main = Main()
    main.execute()