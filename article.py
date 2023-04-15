from config import article_save_status
from bs4 import BeautifulSoup
from slugify import slugify
import time
import phpserialize

class Article:
    log_CateID = None #
    log_AuthorID = 1
    log_Tag = None #
    log_Status = None #
    log_Type = 0
    log_Alias = None #
    log_IsTop = 0
    log_IsLock = 0
    log_Title = None #
    log_Intro = None #
    log_Content = None #
    log_CreateTime = None #
    log_PostTime = None #
    log_UpdateTime = None #
    log_CommNums = 0
    log_ViewNums = 0
    log_Template = ''
    log_Meta = '' #
    dict_data = {}

    def __init__(self, cate_id, title, content, keywords, db=None):
        self.log_CateID = cate_id
        self.log_Title = title
        self.log_Content = content
        self.keywords = keywords
        self.handle_log_Tag(db)
        self.handle_log_Alias()
        self.handle_log_Status()
        self.handle_log_Intro()
        self.handle_log_CreateTime()
        self.handle_log_PostTime()
        self.handle_log_UpdateTime()
        self.handle_log_Meta()
        self.genereate_data()

    def handle_log_Tag(self, db=None):
        if db:
            key_str = ''
            for key in self.keywords:
                key_result = db.table('zbp_tag').where('tag_Name', key.strip()).first()
                if key_result:
                    key_str += '{' + str(key_result['tag_ID']) + '}'
                else:
                    tag_id = db.table('zbp_tag').insert_get_id(
                        {
                            'tag_Name': key.strip(),
                            'tag_Count': 1,
                            'tag_Intro': key.strip(),
                            'tag_Meta': '',
                        }
                    )
                    key_str += '{' + str(tag_id) + '}'
            self.log_Tag = key_str if key_str else None
    
    def handle_log_Status(self):
        self.log_Status = article_save_status

    def handle_log_Alias(self, db=None):
        self.log_Alias = slugify(self.log_Title, allow_unicode=True)

    def handle_log_Intro(self, db=None):
        content_soap = BeautifulSoup(self.log_Content, 'html.parser')
        fst_content = content_soap.find('p').text if content_soap.find('p') else None 
        if fst_content:
            self.log_Intro = '<h1>{}</h1><p>{}</p>'.format(self.log_Title, fst_content)

    def handle_log_CreateTime(self, db=None):
        self.log_CreateTime = int(time.time())

    def handle_log_PostTime(self, db=None):
        if self.log_Status == 0:
            self.log_PostTime = int(time.time())

    def handle_log_UpdateTime(self, db=None):
        self.log_UpdateTime = int(time.time())

    def handle_log_Meta(self, db=None):
        meta = {
            'editor_keyword': self.log_Title,
            'editor_related': self.log_Title,
            'content_keywords': ' '.join(self.keywords)
        }
        
        meta_serialized = phpserialize.dumps(meta)
        self.log_Meta = meta_serialized

    def genereate_data(self):
        self.dict_data['log_CateID'] = self.log_CateID
        self.dict_data['log_AuthorID'] = self.log_AuthorID
        self.dict_data['log_Tag'] = self.log_Tag
        self.dict_data['log_Status'] = self.log_Status
        self.dict_data['log_Type'] = self.log_Type
        self.dict_data['log_Alias'] = self.log_Alias
        self.dict_data['log_IsTop'] = self.log_IsTop
        self.dict_data['log_IsLock'] = self.log_IsLock
        self.dict_data['log_Title'] = self.log_Title
        self.dict_data['log_Intro'] = self.log_Intro
        self.dict_data['log_Content'] = self.log_Content
        self.dict_data['log_CreateTime'] = self.log_CreateTime
        self.dict_data['log_PostTime'] = self.log_PostTime
        self.dict_data['log_UpdateTime'] = self.log_UpdateTime
        self.dict_data['log_CommNums'] = self.log_CommNums
        self.dict_data['log_ViewNums'] = self.log_ViewNums
        self.dict_data['log_Template'] = self.log_Template
        self.dict_data['log_Meta'] = self.log_Meta

    def get_post_dict(self):
        return self.dict_data
