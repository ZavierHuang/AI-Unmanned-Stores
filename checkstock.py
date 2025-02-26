import sqlite3
from linebot import LineBotApi
from linebot.models import *
from datetime import datetime


def renewstock(sellcup,sellbottle,sellbeverage,sellbrush):
    dbcup=0
    dbbottle=0
    dbbeverage=0
    dbbrush=0
    dbid="1"
    quantitycup=int(sellcup)
    quantitybottle=int(sellbottle)
    quantitybeverage=int(sellbeverage)
    quantitybrush=int(sellbrush)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select cup,bottle,beverage,brush from stock" 
    cursor.execute(sqlstr)
    for row in cursor:
        dbcup=int(row[0])
        dbbottle=int(row[1])
        dbbeverage=int(row[2])
        dbbrush=int(row[3])
    dbcup=dbcup-quantitycup
    dbbottle=dbbottle-quantitybottle
    dbbeverage=dbbeverage-quantitybeverage
    dbbrush=dbbrush-quantitybrush
    strdbcup=str(dbcup)
    strdbbottle=str(dbbottle)
    strdbbeverage=str(dbbeverage)
    strdbbrush=str(dbbrush)

    sqlstr= "UPDATE stock SET cup='"+strdbcup+"' WHERE ID='"+dbid+"'"
    cursor.execute(sqlstr)
    conn.commit()
    sqlstr= "UPDATE stock SET bottle='"+strdbbottle+"' WHERE ID='"+dbid+"'"
    cursor.execute(sqlstr)
    conn.commit()
    sqlstr= "UPDATE stock SET beverage='"+strdbbeverage+"' WHERE ID='"+dbid+"'"
    cursor.execute(sqlstr)
    conn.commit()
    sqlstr= "UPDATE stock SET brush='"+strdbbrush+"' WHERE ID='"+dbid+"'"
    cursor.execute(sqlstr)
    conn.commit()

    if(dbcup<3 or dbbottle<3 or dbbeverage<3 or dbbrush<3):
        scup=5
        sbottle=5
        sbeverage=5
        sbrush=5
        scup=scup-dbcup
        sbottle=sbottle-dbbottle
        sbeverage=sbeverage-dbbeverage
        sbrush=sbrush-dbbrush
        strcup=str(scup)
        strbottle=str(sbottle)
        strbeverage=str(sbeverage)
        strbrush=str(sbrush)
        originalstock="5"
        mes="【自動補貨通知】\n"+"此次各產品補充數量如下:\n"+"cup:\t"+strcup+"\n"+"bottle:\t"+strbottle+"\n"+"beverage:\t"+strbeverage+"\n"+"brush:\t\t"+strbrush
        sqlstr= "UPDATE stock SET cup='"+originalstock+"' WHERE ID='"+dbid+"'"
        cursor.execute(sqlstr)
        conn.commit()
        sqlstr= "UPDATE stock SET bottle='"+originalstock+"' WHERE ID='"+dbid+"'"
        cursor.execute(sqlstr)
        conn.commit()
        sqlstr= "UPDATE stock SET beverage='"+originalstock+"' WHERE ID='"+dbid+"'"
        cursor.execute(sqlstr)
        conn.commit()
        sqlstr= "UPDATE stock SET brush='"+originalstock+"' WHERE ID='"+dbid+"'"
        cursor.execute(sqlstr)
        conn.commit()
        line_bot_api = LineBotApi('6XrH++LSNRENXOHtUlDbC61mw5gFfLE3XxP/wy8sJV8NDdU6xAXYkaHrR3YRlMcZLINmAZuRJKguHcFXfPqRQm5Iwn8GeWZkIJs4FlFndyoA8UCuEB8dpDR1YzfLJIrNseCA7hfs18ISien4NB1Z+QdB04t89/1O/w1cDnyilFU=')
        line_bot_api.push_message('Ud794612b57f52bf0e727f2d659020c5a', TextSendMessage(text=mes))#主動推播
        today=datetime.now().strftime('%Y-%m-%d')
        thistime=datetime.now().strftime('%H:%M:%S')
        sqlstr = "INSERT INTO supplementrecord ('date','time','cup','bottle','beverage','brush') VALUES ('"+str(today)+"','"+str(thistime)+"','"+str(strcup)+"','"+str(strbottle)+"','"+str(strbeverage)+"','"+str(strbrush)+"')" 
        cursor.execute(sqlstr)
        conn.commit()
        conn.close()  


    