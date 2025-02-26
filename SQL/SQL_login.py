import sqlite3

def login_data(account_customer,password_customer):
    account=str(account_customer)
    password=str(password_customer)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()

    sqlstr = "CREATE TABLE IF NOT EXISTS company\
        ('ID' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'account' Text Unique,'token' Text)"
    cursor.execute(sqlstr)

    sqlstr = "select account,password,token from company" # choose the all file in table03 -> "select * from table03"
    cursor.execute(sqlstr)

    flag = False
    print("account\tpassword\ttoken")
    for row in cursor:
        print(str(row[0])+'\t'+row[1]+'\t'+row[2]+'\t')
        
        if(str(row[0])==account):
            flag = True
            if(row[1]!=password):
                return ["密碼錯誤",0]
            else:
                return ["登入成功",row[2]]
    if(flag==False):
        return ["此帳號尚未註冊",0]
    


# def analyze():
#     x = login_data("226","abcdefg") 
#     if(x[1]!=0):
#         return x[1]                               # 登入成功
#     else:                                         
#         return x[0];                              # 此電話未註冊 / 密碼錯誤   

# print("-----------------------------------")
# print(analyze())