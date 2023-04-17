gpt_base_url = ''
gpt_token = 'your gpt api key'                                          #required to change
gpt_execute_limit = 4                                                   #in seccondjavascript:;
gpt_messages_init = []
gpt_model_tuning = 'gpt-3.5-turbo'

images_default_path = '/path/to/images/template/default/'               # required to change with absolute path
images_custom_path = '/path/to/images/template/custom/'                 # required to change with absolute path

img_destination_path = "/path/to/destination/path"                      # required to change with absolute path      
img_path_web_relative = "/path/to/dinamyc/path"                         # required to change with relatif path base on img_destination_path
font_path = "/path/to/scriptgpt/font/NotoSansSC_Bold.otf"               # required to change with absolut path

# keyword_list_path = {category_id : keyword_path}
keyword_list_paths = {
    1 : '/www/script/scriptgpt/keyword_list/keyword_list.txt'
}

keyword_length_limit = 1

db_config = {
    'default': 'mysql',
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'example_db',
        'user': 'example_db',
        'password': 'examplepasss',
        'prefix': ''
    }
}

article_save_status = 0