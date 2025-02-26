import sqlite3

def search_data(account,password):
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    
    sqlstr = "CREATE TABLE IF NOT EXISTS company\
        ('ID' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'account' Integer Unique,'password' Text, 'token' Text)"
    cursor.execute(sqlstr)
    
    sqlstr = "select account,password from company" 
    cursor.execute(sqlstr)

    print("account\tpassword")
    for row in cursor:
        print(str(row[0])+'\t'+row[1])

    
    result1 = search_account(account)
    result2 = search_password(password)

    if(result1 != "可註冊帳號"):
        return result1
    if(result2 != "可註冊密碼"):
        return result2
    
    return "可加入"

def search_account(account):
    account=str(account)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account from company" 
    cursor.execute(sqlstr)

    #print("A account")
    for row in cursor:
    #    print(str(row[0]))
        if(str(row[0])==account):
            return "此帳號已註冊，請重新輸入"
    return "可註冊帳號"


def search_password(password):
    password=str(password)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select password from company" 
    cursor.execute(sqlstr)

    #print("B password")
    for row in cursor:
    #    print(str(row[0]))
        if(str(row[0])==password):
            return "此密碼已設定，請重新輸入"
    return "可註冊密碼"

def search_account_number(token):
    token=str(token)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account,token from company" 
    cursor.execute(sqlstr)

    #print("B password")
    for row in cursor:
        print(str(row[0]))
        now_account = str(row[0])
        now_token = str(row[1])
        if(now_token==token):
            return now_account
    return None


def resend_password(account):
    targeted_account=str(account)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account,password,token from company" 
    cursor.execute(sqlstr)

    for row in cursor:
        now_account = str(row[0])
        now_password = str(row[1])
        now_token = str(row[2])
        if(now_account == targeted_account):
            return now_account,now_password,now_token
    return None


