import sqlite3


def create_db():     # 创建数据库
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE USER
        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME TEXT       NOT NULL,
        PASSWORD TEXT NOT NULL);''')
    conn.commit()
    conn.close()

def register(username, password): # 注册
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    print("Opened database successfully");

    c.execute("INSERT INTO USER (NAME,PASSWORD) VALUES (\'{}\',\'{})".format(username,password));

    conn.commit()
    print("Records created successfully username is {username}".format(username=username));
    conn.close()
    return True

def login(username, password): # 登录
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    answer = c.execute("SELECT * FROM USER WHERE NAME = '%s' AND PASSWORD = '%s" %(username,password))
    if answer :
        return True
    return False
# create_db()