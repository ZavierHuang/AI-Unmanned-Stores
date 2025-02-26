import sqlite3
from SQL_search import search_data

def analyze_data(account_customer,password_customer):

    account = str(account_customer)
    password = str(password_customer)

    result = search_data(account,password)
    #print("result:"+result)
    if(result=="此帳號已註冊，請重新輸入"):
        return result
    if(result=="此密碼已設定，請重新輸入"):
        return result
    else:
        return "輸入成功"


def add_data(account_customer,password_customer,token_customer):
    account = str(account_customer)
    password = str(password_customer)
    token = str(token_customer)

    print(account,password,token)

    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()

    sqlstr = "CREATE TABLE IF NOT EXISTS company\
    ('ID' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'account' Text Unique,'password' Text, 'token' Text)"
    cursor.execute(sqlstr)

    sqlstr = "INSERT INTO company ('account','password','token') VALUES ('"+account+"','"+password+"','"+token+"')" 
    cursor.execute(sqlstr)

    # 操作完成，連線更新
    conn.commit()
    conn.close()    
    return "註冊成功"     





#concludsion = add_data("12121212","22222","33333")
#print(concludsion)
