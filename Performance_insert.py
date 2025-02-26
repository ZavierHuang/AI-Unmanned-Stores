import sqlite3
from checkstock import renewstock



def add_item(year_customer,month_customer,day_customer,cup_customer,beverage_customer,bottle_customer,brush_customer,total_customer):
    year = int(year_customer)
    month = int(month_customer)
    day = int(day_customer)
    cup = int(cup_customer)
    bottle = int(bottle_customer)
    beverage = int(beverage_customer)
    brush = int(brush_customer)
    total = int(total_customer)

    print("beverage:",beverage)
    print("bottle:",bottle)

    renewstock(cup,bottle,beverage,brush)
    print(year,month,day)

    conn = sqlite3.connect("D:\Line Notify2_0815\sqlprac.db")
    cursor = conn.cursor()

    sqlstr = "CREATE TABLE IF NOT EXISTS performance\
    ('ID' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,'year' Integer,'month' Integer ,'day' Integer ,'cup' Integer,'bottle' Integer, 'beverage' Integer,'brush' Integer,'total' Integer)"
    cursor.execute(sqlstr)


    sqlstr = "INSERT INTO performance ('year','month','day','cup','bottle','beverage','brush','total') VALUES ('"+str(year)+"','"+str(month)+"','"+str(day)+"','"+str(cup)+"','"+str(bottle)+"','"+str(beverage)+"','"+str(brush)+"','"+str(total)+"')" 

    cursor.execute(sqlstr)

    # 操作完成，連線更新
    conn.commit()
    conn.close()    
    return "輸入成功"     





#concludsion = add_item(2022,9,1,1,2,3,4,500)
#concludsion = add_item(2022,9,2,1,2,3,4,500)
# print(concludsion)
