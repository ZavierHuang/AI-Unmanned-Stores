from flask import Flask, request, abort
from membermanagement import memberlist,searchmember,editmember,delmember,sendpassword
from recordmanagement import todayrecord,particularrecord,periodrecord
from supplementmanagement import searchstock,statisticparticular,statisticperiod,listsupplementrecord

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
import sqlite3
import urllib
import datetime
from urllib import parse
from enum import auto
import requests
from flask import Flask, request
from Performance_insert import add_item
from SQL_insert import analyze_data,add_data
from SQL_login import login_data
from VideoCut import videocut
from Detection import object_detect
from SQL_search import search_account_number,resend_password
import datetime



stack = {"cup":10,"bottle":10,"beverage":10,"bottle":10,"brush":10}

app = Flask(__name__)
flag = False
account=""
password=""
Token=""

'''
使用者訂閱網址：
'''


website = "https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=fr3xPyOztXZD9wfIGdKC3a&redirect_uri=https://b548-2001-b400-e2dd-33ce-3819-fbca-6d9f-582d.ngrok.io&scope=notify&state=NO_STATE"

#Failed to complete tunnel connection #478，解決方法是本地的server要一起執行
def getNotifyToken(AuthorizeCode): # 伺服器的ngrok(redirect_uri)，Client_id以及client_secret
    body = {
        "grant_type": "authorization_code",
        "code": AuthorizeCode,
        "redirect_uri": 'https://b548-2001-b400-e2dd-33ce-3819-fbca-6d9f-582d.ngrok.io',
        "client_id": 'fr3xPyOztXZD9wfIGdKC3a',
        "client_secret": 'VgVOOd7JiEjPBOprHUk32Ko9HbPtyE94O8L3hitcXM9'
    }
    r = requests.post("https://notify-bot.line.me/oauth/token", data=body) # 向伺服器請求得到token
    return r.json()["access_token"]

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return r.status_code

"""
使用者token
"""
#---------------------Enrollment---------------------------#

# @app.route('/')
# def homepage():
#    return 'Hello, World!'


#################################################################################
@app.route('/resend', methods=['GET', 'POST'])        
def resend():
    account = str(request.form['phone'])              
    result = resend_password(account)       
    print("判別結果:",result)
    if result is not None:
        reply = "\n\n [密碼傳送通知]\n\n帳號 ' "+result[0]+" ' 的客戶，密碼 : " + result[1]
        lineNotifyMessage(result[2],reply)     
        return "Resend_Success"
    else:
        return "此帳戶尚未註冊"


#################################################################################


@app.route('/analyze', methods=['GET', 'POST'])        #註冊判別是否正確專用
def handle_request2():
    global account,password
    account = str(request.form['phone'])              
    password = str(request.form['code'])
    conclude = analyze_data(account,password)       
    print("判別結果:"+conclude)
    return conclude                                   #此電話已註冊，請重新輸入/輸入成功/此密碼已設定，請重新輸入

@app.route('/insert', methods=['GET', 'POST'])        #註冊程序
def handle_request3():
    print("ADD Data")
    global account,password,Token
    print("account,password,token:"+account+" "+password+" "+Token)
    conclude = add_data(account,password,Token)       
    print("註冊:"+conclude)
    account=""
    password=""
    Token=""
    return conclude                                  # 註冊成功 


@app.route('/login', methods=['GET', 'POST'])        # 登入專用，若成功則回傳token
def handle_request():
    account = str(request.form['phone'])              
    password = str(request.form['code'])
    result = login_data(account,password)
    print("登入:"+result[0])
    if(result[1]!=0):
        print("token:"+result[1])
        return result[1]                               # 登入成功，回傳token
    return result[0];                                  # 此電話尚未註冊 / 密碼錯誤 


@app.route('/success',methods=['POST','GET'])
def handle_login():
    global flag
    if(flag=="ok"):
        flag="No"
        return "Success"
    else:
        flag="No"
        return "failure"

@app.route('/website',methods=['POST','GET'])
def getwebsite():
    return website

#---------------------Enrollment---------------------------#

@app.route('/', methods=['POST', 'GET'])            #Line notify 連動專用
def hello_world():  # Line notify
    authorizeCode = request.args.get('code')
    token = getNotifyToken(authorizeCode)
    global Token,flag,account,password
    Token = token
    print("Token:",Token)
    flag = "ok"
    lineNotifyMessage(token, "恭喜帳號\""+account+"\"的客戶連動成功")      #lineNotifyMessage(接收者 , 訊息)
    print("account:"+account+" password:"+password+" token:"+Token)
    return f"連動已設定，請按下一步完成註冊"                               #回傳至手機

#---------------------Car Scanning--------------------------#

@app.route('/video_information', methods=['GET', 'POST'])        
def video_information():
    
    start_time = str(request.form['start_time'])              
    finish_time = str(request.form['finish_time'])
    user_token = str(request.form['user_token'])
    fileName = str(request.form['fileName'])

    
    date = start_time.split()[0]
   
    start = start_time.split()[1]
   
    finish = finish_time.split()[1]

    result = "\n親愛的 "+str(search_account_number(user_token))+" 客戶您好\n"
    result = result + "您曾在 "+str(date)+" 光顧賣場\n"
    result = result + "購物時間為 " + str(start) +" ~ "+str(finish)+"\n"
    result = result + "以下為您的購物紀錄與明細\n\n"
    print(result)
    print(start_time)
    print(finish_time)
    print(user_token)
    print(fileName)
    
    videocut(fileName)

    detail,performance,total = object_detect()

    
    result = result + detail
    result = result + "\n\n\n歡迎下次光臨"

    lineNotifyMessage(user_token,result)
    
    if(total!=0):
        date_list = [int(i) for i in date.split('-')]
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
        global stack
        stack["cup"] = stack["cup"]-performance[0]
        stack["beverage"] = stack["beverage"]-performance[1]
        stack["bottle"] = stack["bottle"]-performance[2]
        stack["brush"] = stack["brush"]-performance[3]
        print("stack:",stack)
        add_item(year,month,day,performance[0],performance[1],performance[2],performance[3],total)
        # cup = performance[0]
        # beverage = performance[1]
        # bottle = performance[2]
        # brush = performance[3
    return "Get the movie information"


        
def buy_test():  # 測試用
    detail,performance,total = object_detect()

    result = ""
    result = result + detail
    result = result + "\n\n已自動扣款完成\n\n歡迎下次光臨"

    lineNotifyMessage('byN6yIAGh48WuQMBIqTnwm8FJB2QmYLI0cxbM9J9rD3',result)
    
    tonow = datetime.datetime.now()
    print(tonow.year)
    print(tonow.month)
    print(tonow.day)

    if(total!=0):
        add_item(tonow.year,tonow.month,tonow.day,performance[0],performance[1],performance[2],performance[3],20)


#---------------------linebot--------------------------#
line_bot_api = LineBotApi('15cGiv6b4rw1ZzTzAe+QVHA0y4ykdGPSc1Tj7+5+63Kub0p5Ik/ew+A6qNPuZKvW4F5ZPz3SLu68YjLf9Rp41eQUyI5xdiKMKFGKBiGYtm8RnMudR2GkfuPxxBZp9q/s/9OetOsEtk2GCED7LVJB7wdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('76ef98ed54087ebab5c355358cfe4a1d')

line_bot_api.push_message('Ud3fa7d6b2b4d1e036052cb37bd1d9572', TextSendMessage(text='你可以開始了'))#主動推播

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
flag=0
editact=""
editpwd=""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global flag
    global editact,editpwd
    message = event.message.text#擷取使用者傳送的訊息

#########################################會員管理######################################
    if(flag==1):
        searchact=searchmember(message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(searchact))
        flag=0
        searchact=""
    if(flag==2):
        editact=str(message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入新密碼"))
        flag=3
    if(flag==3):
        editpwd=str(message)
        editmember(editact,editpwd)
        searchact=searchmember(editact)
        searchact="更新後的資料:"+"\n"+searchact
        line_bot_api.reply_message(event.reply_token,TextSendMessage(searchact))
        flag=0
        editact=""
        editpwd=""
    if(flag==4):
        delaccount=str(message)
        delconsult=delmember(delaccount)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(delconsult))
        flag=0
    if(flag==5):
        sendaccount=str(message)
        consult=sendpassword(sendaccount)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(consult))
        flag=0

    if re.match('搜尋會員',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入會員帳號"))
        flag=1
    # if re.match('修改會員密碼',message):
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入會員帳號"))
    #     flag=2
    if re.match('刪除會員',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入會員帳號"))
        flag=4
    # if re.match('重送密碼',message):
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入會員帳號"))
    #     flag=5

    ##################################交易管理#######################################
    if re.match('特定日期業績查詢',message):
        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入欲查詢日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=particulardate&itemid=1',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']

    if re.match('區間業績統計',message):
        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入起始日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=startdate&itemid=2',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']
    
    if re.match('今日營業額查詢',message):
        sellconsult=todayrecord()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(sellconsult))
    
############################庫存管理#########################################
    if re.match('庫存量查詢',message):
        sendmessage=searchstock()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(sendmessage))
    
    if re.match('特定日期補貨紀錄查詢',message):
        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入欲查詢日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=supplementparticulardate&itemid=4',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']


    
    if re.match('區間補貨紀錄查詢',message):
        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入起始日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=supplementperiodstartdate&itemid=5',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']


    if re.match('區間補貨紀錄詳細資訊',message):
        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入起始日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=listsupplementstartdate&itemid=7',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']
    
############################圖文看板#########################################
    if re.match('交易管理',message):
        buttons_template_message = TemplateSendMessage(
         alt_text='這個看不到',
         template=ButtonsTemplate(
             thumbnail_image_url="https://play-lh.googleusercontent.com/RkxrtGFt-S8d_N8Fg8iOKtPBbmCxU9A6Eg6SlGKEiaL5c8PwphupcS22eSAzRJp7w8Fu",
             title='智慧購物車',
             text='交易管理選單',
             actions=[
                 MessageAction(
                     label='今日營業額查詢',
                     text='今日營業額查詢'
                    ),
                 MessageAction(
                     label='特定日期業績查詢',
                     text='特定日期業績查詢'
                    ),
                 MessageAction(
                     label='區間業績統計',
                     text='區間業績統計'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    



    if re.match('會員管理',message):
        buttons_template_message = TemplateSendMessage(
         alt_text='會員管理選單',
         template=ButtonsTemplate(
             thumbnail_image_url='https://play-lh.googleusercontent.com/RkxrtGFt-S8d_N8Fg8iOKtPBbmCxU9A6Eg6SlGKEiaL5c8PwphupcS22eSAzRJp7w8Fu',
             title='智慧購物車',
             text='會員管理選單',
             actions=[
                 MessageAction(
                     label='搜尋會員',
                     text='搜尋會員'
                    ),
                 MessageAction(
                     label='刪除會員',
                     text='刪除會員'
                    ),
                #  MessageAction(
                #      label='重送密碼',
                #      text='重送密碼'
                #     ),
                #  MessageAction(
                #      label='修改會員密碼',
                #      text='修改會員密碼'
                #     )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)


    if re.match('庫存管理',message):
        buttons_template_message = TemplateSendMessage(
         alt_text='庫存管理選單',
         template=ButtonsTemplate(
             thumbnail_image_url='https://play-lh.googleusercontent.com/RkxrtGFt-S8d_N8Fg8iOKtPBbmCxU9A6Eg6SlGKEiaL5c8PwphupcS22eSAzRJp7w8Fu',
             title='智慧購物車',
             text='庫存管理選單',
             actions=[
                 MessageAction(
                     label='庫存量查詢',
                     text='庫存量查詢'
                    ),
                 MessageAction(
                     label='特定日期補貨紀錄查詢',
                     text='特定日期補貨紀錄查詢'
                    ),
                 MessageAction(
                     label='區間補貨紀錄查詢',
                     text='區間補貨紀錄查詢'
                    ),
                 MessageAction(
                     label='區間補貨紀錄詳細資訊',
                     text='區間補貨紀錄詳細資訊'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)



##############################################################################
syear=0
smonth=0
sday=0
startbackdate=""

@handler.add(PostbackEvent)
def getdate(event):
    global syear,smonth,sday,startbackdate,psstartbackdate,pssyear,pssmonth,pssday,lsstartbackdate,lssyear,lssmonth,lssday
    backdata=dict(parse.parse_qsl(event.postback.data))
    if(backdata.get('action')=='particulardate'):
        backdate=str(event.postback.params.get('date'))
        datesplit=backdate.split('-')
        pyear=int(datesplit[0])
        pmonth=int(datesplit[1])
        pday=int(datesplit[2])
        print(pyear)
        print(pmonth)
        print(pday)
        psellitem=particularrecord(pyear,pmonth,pday)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(psellitem))


    if(backdata.get('action')=='startdate'):
        startbackdate=str(event.postback.params.get('date'))
        startdatesplit=startbackdate.split('-')
        syear=str(startdatesplit[0])
        smonth=str(startdatesplit[1])
        sday=str(startdatesplit[2])


        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入結束日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=enddate&itemid=3',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']
        
    if(backdata.get('action')=='enddate'):
        endbackdate=str(event.postback.params.get('date'))
        enddatesplit=endbackdate.split('-')
        eyear=str(enddatesplit[0])
        emonth=str(enddatesplit[1])
        eday=str(enddatesplit[2])
        #global syear,smonth,sday,startbackdate
        periodsellitem=periodrecord(int(syear),int(smonth),int(sday),int(eyear),int(emonth),int(eday))
        reply = str(syear) + "/" + str(smonth) + "/" + str(sday) + " ~ "
        reply += str(eyear) + "/" + str(emonth) + "/" + str(eday) +"\n\n"
        reply += periodsellitem
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reply))
    
    if(backdata.get('action')=='supplementparticulardate'):
        particularbackdate=str(event.postback.params.get('date'))
        datesplit=particularbackdate.split('-')
        pyear=int(datesplit[0])
        pmonth=int(datesplit[1])
        pday=int(datesplit[2])
        particularsup=statisticparticular(pyear,pmonth,pday)
        particularsup=str(pyear)+"年"+str(pmonth)+"月"+str(pday)+"日"+"\n"+particularsup
        line_bot_api.reply_message(event.reply_token,TextSendMessage(particularsup))


    if(backdata.get('action')=='supplementperiodstartdate'):
        psstartbackdate=str(event.postback.params.get('date'))
        psstartdatesplit=psstartbackdate.split('-')
        pssyear=str(psstartdatesplit[0])
        pssmonth=str(psstartdatesplit[1])
        pssday=str(psstartdatesplit[2])


        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入結束日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=supplementperiodenddate&itemid=6',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']

    if(backdata.get('action')=='supplementperiodenddate'):
        psendbackdate=str(event.postback.params.get('date'))
        psenddatesplit=psendbackdate.split('-')
        pseyear=str(psenddatesplit[0])
        psemonth=str(psenddatesplit[1])
        pseday=str(psenddatesplit[2])
        pstatistic=statisticperiod(int(pssyear),int(pssmonth),int(pssday),int(pseyear),int(psemonth),int(pseday))
        reply = str(pssyear) + "/" + str(pssmonth) + "/" + str(pssday) + " ~ "
        reply += str(pseyear) + "/" + str(psemonth) + "/" + str(pseday) +"\n\n"
        reply += pstatistic
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reply))


    if(backdata.get('action')=='listsupplementstartdate'):
        lsstartbackdate=str(event.postback.params.get('date'))
        lsstartdatesplit=lsstartbackdate.split('-')
        lssyear=str(lsstartdatesplit[0])
        lssmonth=str(lsstartdatesplit[1])
        lssday=str(lsstartdatesplit[2])

        date_picker = TemplateSendMessage(
        alt_text='設定日期',
        template=ButtonsTemplate(
            text='輸入結束日期',
            title='YYYY-MM-dd',
            actions=[
                DatetimePickerTemplateAction(
                    label='輸入',
                    data='action=listsupplementenddate&itemid=8',
                    mode='date',
                    initial='',
                    min='2000-01-01',
                    max='2099-12-31'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,date_picker)
        if isinstance(event, PostbackEvent):
            event.postback.params['date']

    if(backdata.get('action')=='listsupplementenddate'):
        lsendbackdate=str(event.postback.params.get('date'))
        lsenddatesplit=lsendbackdate.split('-')
        lseyear=str(lsenddatesplit[0])
        lsemonth=str(lsenddatesplit[1])
        lseday=str(lsenddatesplit[2])
        listrecord=listsupplementrecord(int(lssyear),int(lssmonth),int(lssday),int(lseyear),int(lsemonth),int(lseday))
        reply = str(lssyear) + "/" + str(lssmonth) + "/" + str(lssday) + " ~ "
        reply += str(lseyear) + "/" + str(lsemonth) + "/" + str(lseday) +"\n\n"
        reply += listrecord
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reply))


#---------------------linebot--------------------------#

if __name__ == '__main__':
    #lineNotifyMessage("0MUwqTGe9fQ5hufQS57L5m9CkIQ8u0SbCBdiAASpKif","你好")
    # buy_test()
    app.run(host="0.0.0.0",debug=True)
    




"""
1.創建一個notify應用服務
2.拿著ClientID取得生成給使用者的訂閱網址
3.以此訂閱網址進行訂閱
4.訂閱後會回傳一個金鑰，再以此金鑰向Line notify申請一個可以發送給使用者的token
5.之後以此token發送訊息給使用者



redirect_url (ngrok): 創建一個伺服器(flask)，接收訊息和使用者的訂閱，使用者訂閱後會生成一個金鑰，並以此金鑰和
Line notify 申請一個能夠發送給使用者的token，之後即可以此token發送訊息給使用者
"""