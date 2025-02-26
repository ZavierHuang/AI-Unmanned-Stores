import sqlite3
import datetime

def todayrecord():
    flag=0
    totalcup=0
    totalbottle=0
    totalbeverage=0
    totalbrush=0
    totaltotal=0
    today = datetime.date.today()
    tdyear=today.year
    tdmonth=today.month
    tdday=today.day

    reply = str(tdyear)+"年"+str(tdmonth)+"月"+str(tdday)+"日"+"\n\n"

    deal = 0
    price = [250,20,40,50]  

    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select year,month,day,cup,bottle,beverage,brush,total from performance" 
    cursor.execute(sqlstr)
    for row in cursor:
        if(str(row[0])==str(tdyear) and str(row[1])==str(tdmonth) and str(row[2])==str(tdday)):
            deal += 1
            totalcup=totalcup+int(row[3])
            totalbottle=totalbottle+int(row[4])
            totalbeverage=totalbeverage+int(row[5])
            totalbrush=totalbrush+int(row[6])
            totaltotal=totaltotal+int(row[7])
            flag=1

    reply += "今日之交易量 : %3d 筆\n\n"%(deal)

    if(flag==1):
        cupstr=str(totalcup)
        bottlestr=str(totalbottle)
        beveragestr=str(totalbeverage)
        brushstr=str(totalbrush)
        totalstr=str(totaltotal)
        reply += "[      Cup       ] x " + "%-4s"%(cupstr)    +"/ $ "+str(price[0]*int(cupstr))+"\n"
        reply += "[  Milk  Tea  ] x "    + "%-4s"%(beveragestr)+"/ $ "+str(price[1]*int(beveragestr))+"\n"
        reply += "[ Green Tea ] x "      + "%-4s"%(bottlestr)+"/ $ "+str(price[2]*int(bottlestr))+"\n"
        reply += "[     Brush     ] x "  + "%-4s"%(brushstr)  +"/ $ "+str(price[3]*int(brushstr))+"\n"
        reply = reply + "\n今日總收益為 " + str(totalstr)+" 元"
        return reply
    if(flag==0):
        return reply+"\n查無交易資料"

def particularrecord(particularyear,particularmonth,particularday):
    flag=0
    totalcup=0
    totalbottle=0
    totalbeverage=0
    totalbrush=0
    totaltotal=0
    pyear=particularyear
    pmonth=particularmonth
    pday=particularday

    reply = str(pyear)+"年"+str(pmonth)+"月"+str(pday)+"日"+"\n\n"

    deal = 0
    price = [250,20,40,50]  

    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select year,month,day,cup,bottle,beverage,brush,total from performance" 
    cursor.execute(sqlstr)
    for row in cursor:
        if(str(row[0])==str(pyear) and str(row[1])==str(pmonth) and str(row[2])==str(pday)):
            deal += 1
            totalcup=totalcup+int(row[3])
            totalbottle=totalbottle+int(row[4])
            totalbeverage=totalbeverage+int(row[5])
            totalbrush=totalbrush+int(row[6])
            totaltotal=totaltotal+int(row[7])
            flag=1

    reply += "總交易量 : %3d 筆\n\n"%(deal)

    if(flag==1):
        cupstr=str(totalcup)
        bottlestr=str(totalbottle)
        beveragestr=str(totalbeverage)
        brushstr=str(totalbrush)
        totalstr=str(totaltotal)
        reply += "[      Cup       ] x " + "%-4s"%(cupstr)    +"/ $ "+str(price[0]*int(cupstr))+"\n"
        reply += "[  Milk  Tea  ] x "    + "%-4s"%(beveragestr)+"/ $ "+str(price[1]*int(beveragestr))+"\n"
        reply += "[ Green Tea ] x "      + "%-4s"%(bottlestr)+"/ $ "+str(price[2]*int(bottlestr))+"\n"
        reply += "[     Brush     ] x "  + "%-4s"%(brushstr)  +"/ $ "+str(price[3]*int(brushstr))+"\n"
        reply = reply + "\n總收益為 " + str(totalstr)+" 元"
        return reply
    if(flag==0):
        return reply+"\n查無交易資料"


def periodrecord(startyear,startmonth,startday,endyear,endmonth,endday):
    flag=0
    totalcup=0
    totalbottle=0
    totalbeverage=0
    totalbrush=0
    totaltotal=0
    syear=startyear
    smonth=startmonth
    sday=startday
    eyear=endyear
    emonth=endmonth
    eday=endday
    startdate=datetime.date(syear,smonth,sday)
    enddate=datetime.date(eyear,emonth,eday)
    if(startdate>enddate):
        return "輸入錯誤,起始日期應大於結束日期"

    deal = 0
    price = [250,20,40,50]  
    
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select year,month,day,cup,bottle,beverage,brush,total from performance" 
    cursor.execute(sqlstr)
    for row in cursor:
        startdate = datetime.date(syear,smonth,sday)
        enddate = datetime.date(eyear,emonth,eday)
        datadate=datetime.date(row[0],row[1],row[2])
        if(datadate>startdate and enddate>datadate):
            deal += 1
            totalcup=totalcup+int(row[3])
            totalbottle=totalbottle+int(row[4])
            totalbeverage=totalbeverage+int(row[5])
            totalbrush=totalbrush+int(row[6])
            totaltotal=totaltotal+int(row[7])
            flag=1
        if(datadate==startdate and startdate!=enddate):
            deal += 1
            totalcup=totalcup+int(row[3])
            totalbottle=totalbottle+int(row[4])
            totalbeverage=totalbeverage+int(row[5])
            totalbrush=totalbrush+int(row[6])
            totaltotal=totaltotal+int(row[7])
            flag=1
        if(datadate==enddate and startdate!=enddate):
            deal += 1
            totalcup=totalcup+int(row[3])
            totalbottle=totalbottle+int(row[4])
            totalbeverage=totalbeverage+int(row[5])
            totalbrush=totalbrush+int(row[6])
            totaltotal=totaltotal+int(row[7])
            flag=1
        if(startdate==enddate and datadate==startdate):
            deal += 1
            totalcup=totalcup+int(row[3])
            totalbottle=totalbottle+int(row[4])
            totalbeverage=totalbeverage+int(row[5])
            totalbrush=totalbrush+int(row[6])
            totaltotal=totaltotal+int(row[7])
            flag=1

    reply = "總交易量 : %3d 筆\n\n"%(deal)

    if(flag==1):
        cupstr=str(totalcup)
        bottlestr=str(totalbottle)
        beveragestr=str(totalbeverage)
        brushstr=str(totalbrush)
        totalstr=str(totaltotal)
        reply += "[      Cup       ] x " + "%-4s"%(cupstr)    +"/ $ "+str(price[0]*int(cupstr))+"\n"
        reply += "[  Milk  Tea  ] x "    + "%-4s"%(beveragestr)+"/ $ "+str(price[1]*int(beveragestr))+"\n"
        reply += "[ Green Tea ] x "      + "%-4s"%(bottlestr)+"/ $ "+str(price[2]*int(bottlestr))+"\n"
        reply += "[     Brush     ] x "  + "%-4s"%(brushstr)  +"/ $ "+str(price[3]*int(brushstr))+"\n"
        print("Type:",type(totalstr))
        reply = reply + "\n總收益為 " + str(totalstr) +" 元"
        return reply
    if(flag==0):
        return "查無交易資料"

    


