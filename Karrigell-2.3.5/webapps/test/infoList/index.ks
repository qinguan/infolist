import simpledb
info = simpledb.read('infoList.db')
buss = simpledb.read('bussiness.db')

def index():
#    print '<img src= "tel.jif">'
    print "<h1>Info List</h1>"
    print '<iframe src="http://m.weather.com.cn/m/p5/weather1.htm" width="480" height="150" marginwidth="0" \
    marginheight="0" hspace="0" vspace="0" frameborder="0" scrolling="No" c1=ff0000></iframe><br>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<body bgcolor = "#6666ff">'
#    print '<img src="xscj0089.jif">'   
    
    # login / logout
    print '<body>'
    logged = hasattr(Session(),"user") and Session().user is not None
    if logged:
        print 'Logged in as %s<br>' %Session().user
        print '<a href="logout">Logout</a><p>'
    else:
        print '<a href="login">Login</a><p>'

    # print existing records
    if logged:
        if info:
           print '<table border="3" width="480">'
           print '<tr><th>Name</th><th>Tel</th><th>Emily</th><th>Address</th><th>Func1</th><th>Func2</th></tr>'
           for num,(name,tel,Emily,address) in enumerate(info):
               print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(name, tel ,Emily ,address)
               if logged:
                   print '<td><a href="edit?num=%s">Edit</a></td>' %num
                   print '<td><a href="remove?num=%s">Remove</a></td>' %num
               print '</tr>'
           print '</table><p>'
        else:
           print "No Person in the infoList<p>"

    # prompt logged in users to enter a new record,sort the infoList,search person
        print '<a href="new_person">Enter new Person</a><p>'
        print '<td><a href="info_sort">Sort the infoList by name</a></td><p>'
        print '<td><a href="check_person">Search Person</a></td><p>'
        
    # display the bussiness information  
       
        print '<h4>Memorandum<h4><p>'
        if buss:
            print '<table border="3" width="480" >'         
            print '<tr><th>Time</th><th>Bussiness</th></th><th>Func1</th><th>Func2</th></tr>'
            for num,(time,bussiness) in enumerate(buss):
                print '<tr><td>%s</td><td>%s</td>' %(time,bussiness)
     #           if logged:          
                print '<td><a href="modify?num=%s">Modify</a></td>' %num
                print '<td><a href="delete?num=%s">Delete</a></td>' %num
                print '</tr>'
                print '</table><br>'                  
        else:
            print "No Bussiness in the infoList !<p>"
        print '<a href="new_bussiness">Enter new Bussiness</a><p>'
#        print '<td><a href="memorandum">Memorandum</a></td><p>'

    # page counter
    Include('../counter.py',counter_file='counter.txt')
    print '</body>'

def login():
    print '<body>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<h1>Login</h1>'
    print '<body bgcolor = "#6666ff">'
    print '<form action="check_login" method="post">'
    print 'Login: <br><input name="login"><br><br>'
    print 'Password: <br><input type="password" name="passwd"><br><br>'
    print '<input type="submit" value="Ok">'
    print '</form>'
    print '</body>'
    
    #check the information of the login person 
def check_login(login,passwd):
    if login=="qinguan" and passwd=="qinguan":
        Session().user = login
        print "logged in"
    else:
        print "try again"
    raise HTTP_REDIRECTION,"index"
        
def logout():
    Session().user = None
    raise HTTP_REDIRECTION,"index"

    #input a new person's information
def new_person():
    print '<body>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<h1>New Person</h1>'
    print '<body bgcolor = "#6666f">'
    print '<form action="insert_new_person" method="post">'
    print 'Name: <br><input name="name"><br><br>'
    print 'Tel: <br><input name="tel"><br><br>'
    print 'Emily: <br><input name="Emily"><br><br>'
    print 'address: <br><input name="address"><br><br>'
    print '<input type="submit" value="Ok">'
    print '</form>'
    print '</body>'

def new_bussiness():
    print '<body>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<h1>New Bussiness</h1>'
    print '<body bgcolor = "#6666ff">'
    print '<form action="insert_new_bussiness" method="post">'
    print 'Time: <br><input name="time"><br><br>'
    print 'Bussiness: <br><input name="bussiness"><br><br>'
    print '<input type="submit" value="Ok">'
    print '</form>'
    print '</body>'

def insert_new_bussiness(time,bussiness):
    buss.append((time,bussiness))
    simpledb.save(buss,'bussiness.db')
 #   simpledb.sort_content('infoList.db')
    raise HTTP_REDIRECTION,"index"

    #insert a new person's information
def insert_new_person(name,tel,Emily,address):
    info.append((name,tel,Emily,address))
    simpledb.save(info,'infoList.db')
    raise HTTP_REDIRECTION,"index"

    #sort the info by person's name
def info_sort():
    simpledb.sort_content('infoList.db')
    raise HTTP_REDIRECTION,"index"

    #search the person
def check_person():
    print '<body>'
    print '<h1>Check person</h1>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<body bgcolor = "#6666ff">'
    print '<h4>Name:</h4>'
    print '<form action = "match" method="post">'
    print '<Name: <br><input name = "name"><br><br>'
    print '<input type="submit" value="Ok">'
    print '</form>'
    print '</body>'
    
    #mathe the person's information
def match(name):
    print '<body>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<body bgcolor = "#6666ff">'      
    exist=0
    for i in range(len(info)):
        if name in info[i]:           
            print '<br><h3>The person is already existing !</h3>'           
            print '<table border="3">'
            print '<tr><th>Name</th><th>Tel</th><th>Emily</th><th>address</th><th></tr>'
            name, tel ,Emily ,address = info[i]
            print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(name, tel ,Emily ,address)
            print '</table><p>'
            print '<td><a href="return_last"><h4>return</h4></a></td><p>'          
            exist=1
    if not exist:
        print "<h3>No Person in the infoList !<h3><p>"
        print '<td><a href="return_last"><h4>return</h4></a></td><p>' 
    print '</body>'        
     
     
    #return last page  ......
def return_last():
    print '<td><a href="index"></td><p>'
    raise HTTP_REDIRECTION,"index"

    #edit the person's informaton
def edit(num):
    print '<body>'
    name,tel,Emily,address = info[int(num)]
    print '<h1>New Person</h1>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<body bgcolor = "#6666ff">'
    print '<form action="update_person" method="post">'
    print '<input name="num" type="hidden" value="%s">' %num
    print 'Name: <br><input name="name" value="%s"><br><br>' %name
    print 'Tel: <br><input name="tel" value="%s"><br><br>' %tel
    print 'Emily: <br><input name="Emily" value="%s"><br><br>' %Emily
    print 'Address: <br><input name="address" value="%s"><br><br>' %address
    print '<input type="submit" value="Ok">'
    print '</form>'
    print '</body>'

    #modify the bussiness information    
def modify(num):
    print '<body>'
    time,bussiness = buss[int(num)]
    print '<h1>Modify Bussiness</h1>'
    print '<body topmargin = "100" leftmargin = "360">'
    print '<body bgcolor = "#6666ff">'
    print '<form action="update_bussiness" method="post">'
    print '<input name="num" type="hidden" value="%s"><br>' %num
    print 'Time: <br><input name="time" value="%s"><br><br>' %time
    print 'Bussiness: <br><input name="bussiness" value="%s"><br><br>' %bussiness
    print '<input type="submit" value="Ok">'
 #   print '&nbsp &nbsp &nbsp &nbsp <td><a href="return_last">return</a></td><p>'
    print '</form>'
    print '</body>'
   
    
    #update the person's information    
def update_person(num,name,tel,Emily,address):
 #   info = simpledb.read('infoList.db')
    info[int(num)] = (name,tel,Emily,address)
    simpledb.save(info,'infoList.db')
    raise HTTP_REDIRECTION,"index"

    #update the bussiness information
def update_bussiness(num,time,bussiness):
    buss[int(num)] = (time,bussiness)    
    simpledb.save(buss,'bussiness.db') 
#    simpledb.sort_content('bussiness.db')
    raise HTTP_REDIRECTION,"index"

    #del the person's information
def remove(num):
    del info[int(num)]
    simpledb.save(info,'infoList.db')
    raise HTTP_REDIRECTION,"index"

    #del the bussiness information
def delete(num):
    del buss[int(num)]
    simpledb.save(buss,'bussiness.db')
    raise HTTP_REDIRECTION,"index"



