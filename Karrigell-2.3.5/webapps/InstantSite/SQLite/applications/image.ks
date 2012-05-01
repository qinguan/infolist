"""Database management
Generated 12/26/06 08:21:41"""

base_name = r"C:\cygwin\home\Karrigell\webapps\instantsite\test_sqlite"
name = "image"
fields = (("id","INTEGER","input"),("name","TEXT","input"),("age","INTEGER","input"),("birth","TEXT","input"))
__id__ = "_ROWID_"
import os
from HTMLTags import *
import md5

import k_config

import sys
import traceback

try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    print "SQLite is not installed"
    raise SCRIPT_END

def makeDict(res):
    # convert the result of a cursor.fetchall() to a list
    # of dictionaries
    records = []
    for item in res:
        records.append(dict([(fname,item[i])
            for (i,fname) in enumerate([__id__]+field_names)]))
    return records

field_names = [ f[0] for f in fields ]

# open connection
connection = sqlite.connect(base_name)
cursor = connection.cursor()

#header
header=HEAD(LINK(rel="stylesheet",href="../default.css") +
    TITLE(name))

user_test = hasattr(Session(),'image_user')

def index():
    print '<html>\n'
    print header
    print H1(name)
    if not user_test:
        print '<p><a href="login">Login</p>'
    	raise SCRIPT_END
    # select all the items and return a list of dictionaries, one
    # for each record, indexed by the field names
    cursor.execute('SELECT %s FROM %s' %(','.join(["_ROWID_"]+field_names),name))
    records = makeDict(cursor.fetchall())

    if records:
        print '<table class="main" cellpadding="3" cellspacing="0">'
        print '<tr>'
        print Sum([TH(f,Class="main") for f in field_names])
        if user_test:
            print TH('&nbsp;',Class="main")*2
        print '</tr>\n'
        counter = 0
        for record in records:
            counter+=1
            if counter % 2:
                print '<tr class="even">'
            else:
                print '<tr class="odd">'
            for f in field_names:
                print TD(record[f],Class="main")
            print TD(A('Remove',
                href="removeRecord?record_id=%s" %record[__id__]),
                Class="main")
            print TD(A('Edit',
                href="editRecord?record_id=%s" %record[__id__]),
                Class="main")
            print '</tr>'
        print '</table>'
    else:
        print "Empty base"

	print '<p><a href="editRecord?record_id=-1">New record</a>'
	print '<p><a href="logout">Logout</a>'

    print '</body>\n</html>'

def editRecord(record_id):
    record_id=int(record_id)
    print header
    print '<body>'
    print SCRIPT(Type='text/JavaScript',src='../scw.js')
    print '<script>scwDateOutputFormat  = "YYYY-MM-DD"'
    print 'scwDateInputSequence = "YMD"'
    print '</script>'

    if record_id>-1:
        field_string = ','.join(field_names)
        sql = 'SELECT _ROWID_,%s FROM %s WHERE %s = %s' \
            %(field_string,name,__id__,record_id)
        cursor.execute(sql)
        record = makeDict(cursor.fetchall())[0]
        print H1("Editing a record")
    else:
        print H1("New record")
        record=dict([(f,'') for f in field_names])
    
    print '<form action="insertRecord" method="post">'

    print INPUT(type="hidden",name="record_id",value=record_id)
    print '<table>'
    print TR(TD("id")+TD(INPUT(name="id",size="40",value=record["id"])))
    print TR(TD("name")+TD(INPUT(name="name",size="40",value=record["name"])))
    print TR(TD("age")+TD(INPUT(name="age",size="40",value=record["age"])))
    print TR(TD("birth")+TD(INPUT(name="birth",size="40",value=record["birth"])))

    print '</table>'
    print INPUT(type="submit",value="Ok")
    print '</form>'
    print '</body>\n</html>'

def insertRecord(record_id,**untyped_fields):
    """Insert a record
    record_id : record identifier
    untyped_fields : field values as strings"""
    record_id=int(record_id)
    
    # field names except the record identifier (auto increment)
    f_names = [ f for f in field_names if not f == __id__ ]
    field_string = ','.join(f_names)
    # replace single quotes by double quotes
    for (k,v) in untyped_fields.items():
        untyped_fields[k]=v.replace("'","''")
    if record_id == -1:
        vals = ','.join(["'%s'" %untyped_fields[f] for f in f_names])
        sql = 'INSERT INTO %s (%s) VALUES (%s)' \
            %(name,field_string,vals)
    else:
        vals = ','.join(["%s = '%s'" %(k,v) for (k,v) in untyped_fields.iteritems()])
        sql = 'UPDATE %s SET %s WHERE %s = %s' %(name,vals,__id__,record_id)
    sql = unicode(sql,k_config.outputEncoding)
    try:
        cursor.execute(sql)
        connection.commit()
        raise HTTP_REDIRECTION,"index"
    except sqlite.OperationalError:
        print 'Operational error - try again'
        traceback.print_exc(file=sys.stdout)
        cursor.close()
        connection.close()
    raise HTTP_REDIRECTION,"index"

def removeRecord(record_id):
    """Remove the record with identifier record_id"""
    
    sql = 'DELETE FROM %s WHERE %s = %s' %(name,__id__,record_id)
    cursor.execute(sql)
    connection.commit()

    raise HTTP_REDIRECTION,"index"

def login():
    print H1("Login")
    print '<form action="check_login" method="post">'
    print TABLE(
        TR(TD("Login")+TD(INPUT(name="login"))) +
        TR(TD("Password")+
            TD(INPUT(name="password", Type="password"))) +
        TR(TD(INPUT(Type="submit",value="Ok"))+
            TD("&nbsp;"))
        )
    print '</form>'

def check_login(**user_data):
    digest=open("image.ini","rb").read()
    userDigest=digest[:16]
    passwordDigest=digest[16:]

    if (md5.new(user_data['login']).digest()==userDigest \
            and md5.new(user_data['password']).digest()==passwordDigest):
        setattr(Session(),'%s_user' %name, user_data['login'])
        raise HTTP_REDIRECTION,'index'
    else:    
        print "Authentication failed"
        print P(A("Back",href="index"))

def logout():
    Session().close()
    raise HTTP_REDIRECTION,'index'
