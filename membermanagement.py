import sqlite3
import requests
from flask import Flask, request


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    #return r.status_code


#####################################################################################################

def memberlist():

    a=""
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()

    sqlstr = "select account,password,token from company" # choose the all file in table03 -> "select * from table03"
    cursor.execute(sqlstr)

    for row in cursor:
        a=a+str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])+'\n'
    return a

def searchmember(memberact):
    memberaccount=str(memberact)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account,password,token from company" 
    cursor.execute(sqlstr)
    for row in cursor:
        if(str(row[1])==memberaccount):
            mes="會員資料如下:\n"+"會員帳號:\t"+str(row[0])+"\n"+"會員密碼:\t"+str(row[1])+"\n"+'會員token:\n'+str(row[2])
            return mes

    return "查無此會員"
        

def editmember(memberact,newpassword):
    flag=0
    memberaccount=str(memberact)
    memberpassword=str(newpassword)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account,password,token from company" 
    cursor.execute(sqlstr)
    for row in cursor:
        if(str(row[0])==memberaccount):
            flag=1
    if(flag==1):
        sqlstr= "UPDATE company SET password='"+memberpassword+"' WHERE account='"+memberaccount+"'"
        cursor.execute(sqlstr)
        conn.commit()
        return "更改成功"
    if(flag==0):
        return "查無此會員"

def delmember(memberact):
    memberaccount=str(memberact)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account,password,token from company" 
    cursor.execute(sqlstr)
    for row in cursor:
        if(str(row[0])==memberaccount):
            print("memberaccount:",memberaccount)
            sqlstr="DELETE FROM company WHERE account='"+memberaccount+"'"
            cursor.execute(sqlstr)
            conn.commit()
            return "刪除成功" 

    return "查無此會員"

def sendpassword(memberact):
    flag=0
    memberaccount=str(memberact)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select account,password,token from company" 
    cursor.execute(sqlstr)
    for row in cursor:
        if(str(row[0])==memberaccount):
            flag=1
    if(flag==1):
        passwordmes="\n"+"親愛的 "+str(row[0])+" 客戶您好"+"\n"+"以下為您的密碼:"+"\n"+str(row[1])
        lineNotifyMessage(str(row[2]),passwordmes)
        return "傳送成功"
    if(flag==0):
        return "查無此會員"