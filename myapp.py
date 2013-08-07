# -*- coding: utf-8 -*- 
import hashlib, urllib, urllib2, re, time, json
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template
import logging
import re
import httplib
from BeautifulSoup import BeautifulSoup
from myData import NUMBER_QSH, NUMBER_SH, HELP_INFO, PIC_MSG_TPL, \
     TEXT_MSG_TPL, SORRY_MSG, XC_DATA

app = Flask(__name__)
app.debug = True

#homepage just for fun
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')
    return getBBS()
#公众号消息服务器网址接入验证
#需要在公众帐号管理台手动提交, 验证后方可接收微信服务器的消息推送
@app.route('/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

#来自微信服务器的消息推送
@app.route('/weixin', methods=['POST'])
def weixin_msg():
    if verification(request):
        data = request.data
        msg = parse_msg(data)
        if user_subscribe_event(msg):
            return help_info(msg)
        elif is_text_msg(msg):
            content = msg['Content']
            content = content.encode('UTF-8').strip()
            
            #logging.warning(content)
            if content == u'?' or content == u'？':
                return help_info(msg)
            elif content[0:2].lower() == 'gj':
                return response_text_msg(msg, getBUS(content[2:]))
            elif len(content) == 2 and content.lower() == 'tq':
                return response_text_msg(msg, getWether())
            elif len(content) == 2 and content.lower() == 'hp':
                return response_text_msg(msg, getBBS())
            elif len(content) == 2 and content.lower() == 'dk':
                return response_text_msg(msg, getRIEST())
            elif len(content) == 3 and content.lower() == 'qsh':
                return response_text_msg(msg, NUMBER_QSH)
            elif len(content) == 2 and content.lower() == 'sh':
                return response_text_msg(msg, NUMBER_SH)
            elif len(content) == 2 and content.lower() == 'xc':
                return getXC(msg)
            elif len(content) > 2 and content[0:2].lower() == 'kd':
                return response_text_msg(msg, getExpress(content[2:]))
            else :
                return response_text_msg(msg, u'无法识别，请回复"?"查看帮助')
    return 'message processing fail'

def test():
    url = 'http://www.aikuaidi.cn/rest/?key=76b9c59566e54e82909af1f6aa0e46fc&order=028435956303&id=shunfeng&ord=&show=xml'
    return urllib.urlopen(url).read()

def getExpress(order):
    url = 'http://www.aikuaidi.cn/rest/?key=76b9c59566e54e82909af1f6aa0e46fc&order=%s&id=%s&ord=&show=xml'
    ID = ['shentong', 'yuantong', 'yunda', 'shunfeng', 'zhongtong', 'guotong']
    log = ''
    for i in range(6):
        res = urllib.urlopen(url % (order, ID[i])).read()
        soup = BeautifulSoup(res)
        errCode = soup.find('errcode')
        if errCode.string != '0':
            continue
        status = soup.find('status')
        if  status.string == '1':
            continue
        log += soup.find('name').string + ':' + order + '\n'
    
        orders = soup.find('data').findAll('order')
        for o in orders:
            log += o.find('time').string + ':' + o.find('content').string + '\n'
        break
    if log == '':
        return u'暂无记录或者订单号有误,请保证是：顺丰/申通/圆通/韵达/中通/国通！'
    else :
        return log
def getPARAM(httpRes, cookieName):
    coo = httpRes['set-cookie']
    start = coo.find(cookieName) + len(cookieName) + 1
    end = coo.find(";", start)
    return coo[start:end]
def getRIEST():
    url = 'http://riest.uestc.edu.cn/'
    res = urllib.urlopen(url).read()
    soup = BeautifulSoup(res)
    con = soup.find("div", {"class":"panel-content riest-center-column-content"}).findAll('li')
    llen = len(con)
    i = 0
    
    newRiest = u'【最新新闻】\n'
    while i < llen:
        newRiest += '[%d]'%(i+1) + con[i].find('a', title=True).next + '\n'
        i += 1
    con = soup.find("div",{"id":"riest-right-column"}).findAll('a', title=True)
    llen = len(con)
    i = 0
    newRiest += u'【通知公告】\n'
    while i < llen:
        newRiest += '[%d]'%(i+1) + con[i].next + '\n'
        i += 1
    return newRiest
        
def getBBS():
    BBS_HOST = "bbs.qshpan.com"
    UC_HOST = "uc.stuhome.net"
    #bbs2uc
    conn = httplib.HTTPConnection(BBS_HOST)
    conn.request("GET", "/login.php")
    res = conn.getresponse()
    url = res.getheader('location')
    bbsCookie = res.getheader('set-cookie')
    bbs2ucRes = res.msg
    start = url.find('rand=')+5;
    rand = url[start:(start+6)]
    #way2uc
    conn = httplib.HTTPConnection(UC_HOST)
    conn.request("GET", res.getheader('location')[21:])
    res = conn.getresponse()
    ucCookie = res.getheader('set-cookie')
    headers = {'Content-Type':'application/x-www-form-urlencoded', 'Cookie':ucCookie}
    body = {'username':'deartiger', 'password':'22aa1655ac83b9f3e2019a5b9355a4dfdd621e17e28a0111d2b9ea016e03e187dcba6a06a6535a6c680f52a328f107f36ca0a4474d9d2d2481b5a158d7db31918a085036c56d101cf3ccebf46a705658'}
    url = 'http://uc.stuhome.net/admin.php?m=user&a=login&aid=2&rand='+rand
    req = urllib2.Request(url, urllib.urlencode(body))
    req.add_header('Content-Typ', 'application/x-www-form-urlencoded')
    req.add_header('Cookie', ucCookie)
    resp = urllib2.urlopen(req)
    ref = resp.geturl()
    res = resp.read()
    
    #uc2bbs
    start = res.find("redirect('") + 10
    end = res.find("'", start)
    url = res[start:end]
    LASTVISIT = getPARAM(bbs2ucRes, '56f61_lastvisit')
    PHPSESSID = getPARAM(bbs2ucRes, 'PHPSESSID')
    coo = '56f61_lastvisit='+LASTVISIT+'; PHPSESSID='+PHPSESSID
    headers = {'Cookie':coo, 'Referer':ref}
    conn = httplib.HTTPConnection(BBS_HOST)
    conn.request("GET", url[21:], headers = headers)
    res = conn.getresponse()
    header = res.msg
    WINDUSER = getPARAM(header, '56f61_winduser')
    LASTVISIT = getPARAM(header, '56f61_lastvisit')
    #goindex
    coo = '56f61_winduser=' + WINDUSER + '; PHPSESSID' + PHPSESSID + '; 56f61_lastvisit='+LASTVISIT
    headers = {'Cookie':coo, 'Referer':ref}
    conn = httplib.HTTPConnection(BBS_HOST)
    
    conn.request("GET", "/search.php?sch_time=all&orderway=lastpost&asc=desc&newatc=1", headers = headers)
    res = conn.getresponse().read().decode('gbk')
    soup = BeautifulSoup(res)
    con = soup.findAll("div", {"class":"t"})
    con = con[1].findAll('a')
    i = 0
    resCon = u'【清水河畔Top10】\n'
    while i < 10:
        ss = str(con[i*4])
        start = ss.find('>') + 1
        while ss[start] == '<':
            start = ss.find('>', start) + 1
        end = ss.find('<', start)
        resCon += '[%s]'%(str(i+1)) + \
                  unicode(ss[start:end].replace('&nbsp;', ''), 'UTF-8') + '\n'
        
        ss = str(con[i*4+3])
        start = ss.find('>') + 1
        end = ss.find('<', start)
        resCon += ' <' + \
                  unicode(ss[start:end], 'UTF-8').strip() + '>'
        ss = str(con[i*4+2])
        start = ss.find('>') + 1
        end = ss.find('<', start)
        resCon += '['+\
                  unicode(ss[start:end], 'UTF-8') + ']\n'
        i += 1
    return resCon

def getRIEST():
    url = 'http://riest.uestc.edu.cn/'
    res = urllib.urlopen(url).read()
    soup = BeautifulSoup(res)
    con = soup.find("div", {"class":"panel-content riest-center-column-content"}).findAll('li')
    llen = len(con)
    i = 0
    
    newRiest = u'【最新新闻】\n'
    while i < llen:
        newRiest += '[%d]'%(i+1) + con[i].find('a', title=True).next + '\n'
        i += 1
    con = soup.find("div",{"id":"riest-right-column"}).findAll('a', title=True)
    llen = len(con)
    i = 0
    newRiest += u'【通知公告】\n'
    while i < llen:
        newRiest += '[%d]'%(i+1) + con[i].next + '\n'
        i += 1
    return newRiest

def getWether():
    info = u'【成都】'
    url = 'http://m.weather.com.cn/data/101270101.html'
    res = urllib.urlopen(url).read()
    date = re.search(r'(?<="date_y":").*?(?=",")', res).group()
    info += unicode(date, 'UTF-8') + '\n'
    temp = re.findall(r'(?<="temp\d":").*?(?=",")', res)
    weather = re.findall(r'(?<="weather\d":").*?(?=",")', res)
    wind = re.findall(r'(?<="wind\d":").*?(?=",")', res)
    info += u'今天：' + unicode(weather[0], 'UTF-8') + ' ' + unicode(temp[0], 'UTF-8') + ' ' + unicode(wind[0], 'UTF-8') + '\n'
    info += u'明天：' + unicode(weather[1], 'UTF-8') + ' ' + unicode(temp[1], 'UTF-8') + ' ' + unicode(wind[1], 'UTF-8') + '\n'
    info += u'后天：' + unicode(weather[2], 'UTF-8') + ' ' + unicode(temp[2], 'UTF-8') + ' ' + unicode(wind[2], 'UTF-8')
    return info

def getBUS(info):
    info = urllib.quote(info)
    metro = ['%e5%9c%b0%e9%93%811%e5%8f%b7%e7%ba%bf', \
             '%e5%9c%b0%e9%93%812%e5%8f%b7%e7%ba%bf', \
             '%e5%9c%b0%e9%93%813%e5%8f%b7%e7%ba%bf', \
             '%e5%9c%b0%e9%93%814%e5%8f%b7%e7%ba%bf', \
             '%e5%9c%b0%e9%93%815%e5%8f%b7%e7%ba%bf', \
             '%e5%9c%b0%e9%93%816%e5%8f%b7%e7%ba%bf']
    if info.lower() in metro or len(info) < 6:
        route = ''
        url = 'http://m.8684.cn/chengdu_so?k=pp&q=' + info
        if len(info) < 6:
            url = url + '%e8%b7%af'
        res = urllib.urlopen(url).read()
        soup = BeautifulSoup(res)
        con = soup.find("p", {"class":"text_normal_small"})
        if con == None:
            return SORRY_MSG
        while con.next != ' ':
            con = con.next
            if con.find('br') == -1:
                route += con.strip()
            else:
                route += '\r\n'
        #print(route)
        lineTitle = soup.find("ul", {"class":"lineTitle"}).findAll("li")
       
        lineConent = soup.findAll("div", {"class":"lineConent"})
        
        k = 0
        while k < len(lineConent):
            route += ">>>>>" + lineTitle[k].next + "\r\n"
            con = lineConent[k].findAll("span")
            cnt = len(con)
            i = 0
            while i < cnt:
                if i%2 == 0:
                    route += "[%s]"%(con[i].next)
                else:
                    route += con[i].next + "\r\n"
                i += 1
            k += 1
        return route
    else:
        route = ''
        url = 'http://m.8684.cn/chengdu_so?k=p&q=' + info
        #return url
        res = urllib.urlopen(url).read()
        soup = BeautifulSoup(res)
        con = soup.find("ul", {"class":"siteDetails_bus"})
        if con == None:
            return SORRY_MSG
        con = con.findAll("span")
        k = 0
        llen = len(con)
        while k < llen:
            route += ',' + con[k].next
            k += 1
        return route[1:]

#接入和消息推送都需要做校验
def verification(request):
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    token = 'weixint64ago' #注意要与微信公众帐号平台上填写一致
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False

#将消息解析为dict
def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def is_text_msg(msg):
    return msg['MsgType'] == 'text'

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'



def help_info(msg):
    return response_text_msg(msg, HELP_INFO)


def getXC(recvmsg):
    url = 'weixint64ago.sinaapp.com/static/img/xc.jpg'
    msg = PIC_MSG_TPL % (recvmsg['FromUserName'], recvmsg['ToUserName'], 
        str(int(time.time())), XC_DATA, url, url)
    return msg

def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'], 
        str(int(time.time())), content)
    return s
