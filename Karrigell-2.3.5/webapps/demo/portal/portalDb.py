import os
from PyDbLite import Base

db = { 'users':Base(os.path.join(os.getcwd(),'data','users')), 
    'news':Base(os.path.join(os.getcwd(),'data','news')) }
db['users'].create('login','password','bgcolor','fontfamily',
    mode="open")
db['news'].create('login','title','body','date',mode="open")