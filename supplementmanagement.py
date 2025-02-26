import sqlite3
import datetime

def manualsupplement():
    originalstock="5"
    dbid="1"
    dbcup=0
    dbbottle=0
    dbbeverage=0
    dbbrush=0
    scup=5
    sbottle=5
    sbeverage=5
    sbrush=5
    

    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select cup,bottle,beverage,brush from stock" 
    cursor.execute(sqlstr)
    for row in cursor:
        dbcup=int(row[0])
        dbbottle=int(row[1])
        dbbeverage=int(row[2])
        dbbrush=int(row[3])

    scup=scup-dbcup
    sbottle=sbottle-dbbottle
    sbeverage=sbeverage-dbbeverage
    sbrush=sbrush-dbbrush
    strcup=str(scup)
    strbottle=str(sbottle)
    strbeverage=str(sbeverage)
    strbrush=str(sbrush)

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
    mes="【手動補貨完成通知】\n"+"此次各產品補充數量如下:\n"+"cup:\t"+strcup+"\n"+"bottle:\t"+strbottle+"\n"+"beverage:\t"+strbeverage+"\n"+"brush:\t\t"+strbrush
    return mes

def searchstock():
    dbcup=0
    dbbottle=0
    dbbeverage=0
    dbbrush=0
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select cup,bottle,beverage,brush from stock" 
    cursor.execute(sqlstr)
    for row in cursor:
        dbcup=str(row[0])
        dbbottle=str(row[1])
        dbbeverage=str(row[2])
        dbbrush=str(row[3])
    mes="現在各商品庫存數量\n\n"
    mes += "[      Cup       ]  x%4s" %(dbcup) +"\n"
    mes += "[  Milk  Tea  ]  x%4s" %(dbbeverage) +"\n"
    mes += "[ Green Tea ]  x%4s" %(dbbottle) +"\n"
    mes += "[     Brush     ]  x%4s" %(dbbrush) +"\n"
    return mes


def statisticparticular(particularyear,particularmonth,particularday):
    flag=0
    count=0
    totalcup=0
    totalbottle=0
    totalbeverage=0
    totalbrush=0
    totaltotal=0
    strparticularyear=str(particularyear)
    strparticularmonth=str(particularmonth)
    strparticularday=str(particularday)
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select date,cup,bottle,beverage,brush from supplementrecord" 
    cursor.execute(sqlstr)
    for row in cursor:
        particulardate=str(row[0])
        datesplit=particulardate.split("-")
        splityear=datesplit[0]
        tmonth=int(datesplit[1])
        splitmonth=str(tmonth)
        tday=int(datesplit[2])
        splitday=str(tday)
        if(strparticularyear==splityear and strparticularmonth==splitmonth and strparticularday==splitday):
            totalcup=totalcup+int(row[1])
            totalbottle=totalbottle+int(row[2])
            totalbeverage=totalbeverage+int(row[3])
            totalbrush=totalbrush+int(row[4])
            count=count+1
            flag=1
    if(flag==1):
        cupstr=str(totalcup)
        bottlestr=str(totalbottle)
        beveragestr=str(totalbeverage)
        brushstr=str(totalbrush)
        totalstr=str(totaltotal)
        countstr=str(count)
        supplementitem ="\n當日補貨次數:\t"+countstr+"次\n\n"
        supplementitem += "[      Cup       ]  +%3s" %(cupstr) +"\n"
        supplementitem += "[  Milk  Tea  ]  +%3s" %(beveragestr) +"\n"
        supplementitem += "[ Green Tea ]  +%3s" %(bottlestr) +"\n"
        supplementitem += "[     Brush     ]  +%3s" %(brushstr) +"\n"
        return supplementitem
    if(flag==0):
        return "\n查無補貨資料"


def statisticperiod(startyear,startmonth,startday,endyear,endmonth,endday):
    flag=0
    totalcup=0
    totalbottle=0
    totalbeverage=0
    totalbrush=0
    totaltotal=0
    count=0
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
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select date,cup,bottle,beverage,brush from supplementrecord" 
    cursor.execute(sqlstr)
    for row in cursor:
        startdate = datetime.date(syear,smonth,sday)
        enddate = datetime.date(eyear,emonth,eday)
        datadate=str(row[0])
        datesplit=datadate.split("-")
        splityear=int(datesplit[0])
        splitmonth=int(datesplit[1])
        splitday=int(datesplit[2])
        datadate=datetime.date(splityear,splitmonth,splitday)
        if(datadate>startdate and enddate>datadate):
            totalcup=totalcup+int(row[1])
            totalbottle=totalbottle+int(row[2])
            totalbeverage=totalbeverage+int(row[3])
            totalbrush=totalbrush+int(row[4])
            count=count+1
            flag=1
        if(datadate==startdate and startdate!=enddate):
            totalcup=totalcup+int(row[1])
            totalbottle=totalbottle+int(row[2])
            totalbeverage=totalbeverage+int(row[3])
            totalbrush=totalbrush+int(row[4])
            count=count+1
            flag=1
        if(datadate==enddate and startdate!=enddate):
            totalcup=totalcup+int(row[1])
            totalbottle=totalbottle+int(row[2])
            totalbeverage=totalbeverage+int(row[3])
            totalbrush=totalbrush+int(row[4])
            count=count+1
            flag=1
        if(startdate==enddate and datadate==startdate):
            totalcup=totalcup+int(row[1])
            totalbottle=totalbottle+int(row[2])
            totalbeverage=totalbeverage+int(row[3])
            totalbrush=totalbrush+int(row[4])
            count=count+1
            flag=1

    if(flag==1):
        cupstr=str(totalcup)
        bottlestr=str(totalbottle)
        beveragestr=str(totalbeverage)
        brushstr=str(totalbrush)
        totalstr=str(totaltotal)
        countstr=str(count)
        supplementitem="區間補貨次數:\t"+countstr+"\n\n"
        supplementitem += "[      Cup       ]  +%3s" %(cupstr) +"\n"
        supplementitem += "[  Milk  Tea  ]  +%3s" %(beveragestr) +"\n"
        supplementitem += "[ Green Tea ]  +%3s" %(bottlestr) +"\n"
        supplementitem += "[     Brush     ]  +%3s" %(brushstr) +"\n"
        return supplementitem
    if(flag==0):
        return "\n查無補貨資料"


def listsupplementrecord(startyear,startmonth,startday,endyear,endmonth,endday):
    flag=0
    totalcup=0
    totalbottle=0
    totalbeverage=0
    totalbrush=0
    totaltotal=0
    count=0
    mes=""
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
    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()
    sqlstr = "select date,time,cup,bottle,beverage,brush from supplementrecord" 
    cursor.execute(sqlstr)
    for row in cursor:
        startdate = datetime.date(syear,smonth,sday)
        enddate = datetime.date(eyear,emonth,eday)
        datadate=str(row[0])
        datesplit=datadate.split("-")
        splityear=int(datesplit[0])
        splitmonth=int(datesplit[1])
        splitday=int(datesplit[2])
        datadate=datetime.date(splityear,splitmonth,splitday)
    
        if(datadate>startdate and enddate>datadate):
            tempmes = "\n-------------------------------------------\n"
            tempmes += "日期:\t"+str(row[0])+"\n"+"時間:\t"+str(row[1])
            tempmes += "\n-------------------------------------------\n"
            tempmes += "Cup +\t"+str(row[2])+"\n"+"Green Tea +\t"+str(row[3])+"\n"+"Milk Tea +\t"+str(row[4])+"\n"+"Brush +\t"+str(row[5])+"\n"
            mes=mes+tempmes
            count=count+1
            flag=1
        if(datadate==startdate and startdate!=enddate):
            tempmes = "\n-------------------------------------------\n"
            tempmes += "日期:\t"+str(row[0])+"\n"+"時間:\t"+str(row[1])
            tempmes += "\n-------------------------------------------\n"
            tempmes += "Cup +\t"+str(row[2])+"\n"+"Green Tea +\t"+str(row[3])+"\n"+"Milk Tea +\t"+str(row[4])+"\n"+"Brush +\t"+str(row[5])+"\n"
            mes=mes+tempmes
            count=count+1
            flag=1
        if(datadate==enddate and startdate!=enddate):
            tempmes = "\n-------------------------------------------\n"
            tempmes += "日期:\t"+str(row[0])+"\n"+"時間:\t"+str(row[1])
            tempmes += "\n-------------------------------------------\n"
            tempmes += "Cup +\t"+str(row[2])+"\n"+"Green Tea +\t"+str(row[3])+"\n"+"Milk Tea +\t"+str(row[4])+"\n"+"Brush +\t"+str(row[5])+"\n"
            mes=mes+tempmes
            count=count+1
            flag=1
        if(startdate==enddate and datadate==startdate):
            tempmes = "\n-------------------------------------------\n"
            tempmes += "日期:\t"+str(row[0])+"\n"+"時間:\t"+str(row[1])
            tempmes += "\n-------------------------------------------\n"
            tempmes += "Cup +\t"+str(row[2])+"\n"+"Green Tea +\t"+str(row[3])+"\n"+"Milk Tea +\t"+str(row[4])+"\n"+"Brush +\t"+str(row[5])+"\n"
            mes=mes+tempmes
            count=count+1
            flag=1
    
    if(flag==1):
        countstr=str(count)
        sendmes=countstr+" 筆補貨紀錄如下:\n"+mes
        return sendmes
    if(flag==0):
        return "\n查無補貨紀錄"


print(listsupplementrecord(2022,8,15,2022,8,17))
