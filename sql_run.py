from database.sql import selects
from database.sql import *
from collect.instagram_crawling import *
from sql_insta_search_record import *
from sql_insta_contents_record import *
from sql_insta_user_account import *


try:
    put_search_records_all(1,get_insta_keyword())
    put_general_records_all(1,get_insta_keyword())
    put_content_records_all(1,get_insta_userid())
    put_user_account(get_insta_userid())
except:
    print('run_error')






