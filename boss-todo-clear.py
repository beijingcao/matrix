# -*- coding: utf-8 -*-
# 2024-11-02 主要将bossinfo和todolist合并成一个程序；删除u更新的功能；将-功能修改为删除所有相同名字的并更新4-last-total.txt文件
# 2024-11-02 +姓名后主动发送一条当前添加后的结果，如果是唯一的直接显示内容，如果是多条则显示list；讲c的搜索合并到s中；

import simplematrixbotlib as botlib
import sqlite3,re,requests,json,random,urllib.parse,asyncio
from xpinyin import Pinyin
from bs4 import BeautifulSoup

user_agent = [
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
                'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
                'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
                'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
                'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
                'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
                'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
                'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'
            ]
cookie='BAIDUID_BFESS=9E2020DB8E5E50ECE7A0DA2DD288B64D:FG=1; BIDUPSID=9E2020DB8E5E50ECE7A0DA2DD288B64D; PSTM=1725517639; ZFY=lmj7O66w6kHVE7F3vqWKxbr0XnBbl5CzxuVj:AW:ADNSc:C; H_WISE_SIDS=60829; H_PS_PSSID=60841_60853_60884_60875_60898; channel=google; ab_sr=1.0.1_Yzc3ODg4ZDE1YTExNGQ0OWY1YTZhNzBjMDdmMGEwZGM0MjI4MjljYWQ5YzdiNGUzNWI3OTAxZTdmNGIyMWM4NzAzOWM0OGI0NDkwOGE5ODY3YThlMzBhYTg5YjQ4MDlmYTg0Nzg0YmU0NmJiMTI4NTEwNTkxMjE4Njg4YmQxNGIxOWRkZTg5NWI3ZGU1YTUyNDNmYTk1N2YwZmVjYzJiZg==; baikeVisitId=f099ad48-16d0-43c2-88d9-ec3a69d485a3'
Accept_Encoding='gzip, deflate, br, zstd'

config = botlib.Config()
#config.load_toml("./config.toml")
config.encryption_enabled = True  # Automatically enabled by installing encryption support
config.emoji_verify = True
config.ignore_unverified_devices = True
config.store_path = '/root/bossinfo/crypto_store/'
creds = botlib.Creds(
    homeserver="https://www.hwmind.cn",
    username="bossinfo",
    password="ffff@1234",
    session_stored_file="/root/bossinfo/session.txt"
    )
bot = botlib.Bot(creds, config)

###########################全局变量定义###########################
txt_filename='4-last-total.txt'
db_name='boss-todo.db'
boss_db_table='contentlist'
todo_db_table='todolist'
Todo1_db_table='learnlist'

def name_to_py(name):
    PY=Pinyin().get_initials(name, u'')
    py0=PY.lower()
    # print(py0)
    return py0

##############################name to baiduinfo start###############################################
def check_title(strs):
    allcity=['书记','市长','区长','县长','主席','省长','校长','处长','厅长','委员','上将','中将','少将','司令','参谋长','政委','主任','局长','行长','部长','院长','检察长','常委','秘书长','院士']
    checklist = []
    for i in allcity:
        if i in strs:
            checklist.append(1)
            break
        else:
            checklist.append(0)
    if 1 in checklist:
        return 1
    else:
        return 0

#根据有效的名字url查询百度，获取确定内容
def get_baidu_content_with_url(name_url):
    print(name_url)
    headers_page = {'Referer': 'https://baike.baidu.com/', "User-Agent": random.choice(user_agent),"Cookie": cookie,"Accept-Encoding":Accept_Encoding}
    res_page = requests.get(url=name_url, headers=headers_page, timeout=(10, 30))
    html_page = res_page.text
    soup_page = BeautifulSoup(html_page, "html.parser")
    print(soup_page)
    # 查找class为"lemmaDesc_quNQj"的标签并获取其中的文字信息
    # title0 = soup_page.find(class_="lemmaDesc_quNQj")
    pattern0 = re.compile(r'lemmaDescText_(.*?)')
    title0 = soup_page.find(class_=pattern0)
    print(title0)
    # print(1111111)
    if title0:    # print(title)
        content1 = ''
        content2 = ''
        title=title0.get_text()
        # 查找class为"J-lemma-content"下class为"para_pS8cZ content_oCYNu MARK_MODULE"的所有文字信息，并输出段落
        pattern = re.compile(r'lemmaSummary(.*?)J-summary')
        pattern1 = re.compile(r'para_(.*?)summary_(.*?)MARK_MODULE')
        paragraphs01 = soup_page.find(class_=pattern)
        if paragraphs01:
            paragraphs1 = paragraphs01.find_all(class_=pattern1)
            if paragraphs1:
                for paragraph in paragraphs1:
                    jingli = paragraph.get_text()
                    # print(jingli)
                    content1 += jingli + "\n"
                # print(content1)
        else:
            content1 = ''
        # print(paragraphs1)
        pattern2 = re.compile(r'para_(.*?)content_(.*?)MARK_MODULE')
        paragraphs02 = soup_page.find(class_="J-lemma-content")
        if paragraphs02:
            paragraphs2 = paragraphs02.find_all(class_=pattern2)
            if paragraphs2:
                for paragraph in paragraphs2:
                    jingli = paragraph.get_text()
                    # print(jingli)
                    content2 += jingli + "\n"
                # print(content2)
        else:
            content2=''
        if content1=='':
            content=content2
        elif content2=='':
            content = content1
        else:
            content = content1+ "\n"+content2
    else:
        title=''
        content=''
        print('查询个人数据错误')
    return title,content

def send_contents_to_db(name,py,title,content):
    boss_db_table = 'contentlist'
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    query = "INSERT OR IGNORE INTO {} ('name', 'name_py', 'title', 'content') VALUES (?, ?, ?, ?)".format(boss_db_table)
    # 提交更改
    if content:
        cs.execute(query, (name, py, title, content))
        conn.commit()
        conn.close()
#根据name获取有效的baidu url信息，并存入namecontent信息表格
def get_person_4_details_to_db(name):
    # print(name)
    title=''
    content=''
    name_py=name_to_py(name)
    headers_page = {'Referer': 'https://baike.baidu.com/', "User-Agent": random.choice(user_agent),"Cookie": cookie,"Accept-Encoding":Accept_Encoding}
    name0=urllib.parse.quote(name)
    page_url = urllib.parse.urljoin('https://baike.baidu.com/item/', name0)
    # print(page_url)
    res_page = requests.get(url=page_url, headers=headers_page, timeout=(10, 30))
    html_page = res_page.content.decode('UTF-8')
    # print(html_page)
    soup_page = BeautifulSoup(html_page, "html.parser")
    # div_tag = soup_page.find('div', class_='lemmaWrapper_hGgBd')
    pattern = re.compile(r'polysemantText_(.*?)')
    div_tag1 = soup_page.find('div', class_=pattern)
    pattern01 = re.compile(r'contentItem_(.*?)')
    pattern11 = re.compile(r'contentItemChild_(.*?)')
    titles0= soup_page.find(class_=pattern01)
    if div_tag1:#查找是否存在多个同名items，如果存在则查询各个名字的id
        pattern = re.compile(r'<script>window.PAGE_DATA= (.*?)</script>', re.S)
        result = re.search(pattern, html_page)
        if result:
            data = result.group(1)
            # print(data)
            dictionary = json.loads(data.replace("'", '"'))
            # print(data)
            result0=dictionary['navigation']['lemmas']
            # print(result0)
            for i in result0:
                lemmaId=i['lemmaId']
                lemmaDesc=i['lemmaDesc']
                # print(lemmaId,lemmaDesc)
                #检查是否是政府官员或者需要的人员类型
                if check_title(lemmaDesc)==1:
                    page_url = 'https://baike.baidu.com/item/' + name
                    encoded_url = urllib.parse.quote(page_url, safe='/:?=&')
                    # print(encoded_url)
                    list_url = encoded_url+'/'+str(lemmaId)
                    title, content = get_baidu_content_with_url(list_url)
                    print(title,content[0:20])
                    if title:
                        send_contents_to_db(name, name_py, title, content)
                        print('%s %s 完成！' % (name, title))
        else:
            print("未找到同名词条<script>window.PAGE_DATA=匹配的内容")
    elif titles0:#多个同名items显示在item/name页面的处理过程
        titles = titles0.find_all(class_=pattern11)
        for t in titles:
            title = t.get_text()
            tit_url=t['href']
            if check_title(title) == 1:
                page_url = 'https://baike.baidu.com' + tit_url
                # list_url = urllib.parse.quote(page_url, safe='/:?=&')
                # print(f"{text}，URL链接：{list_url}")
                title, content = get_baidu_content_with_url(page_url)
                print(title, content[0:20])
                if title:
                    send_contents_to_db(name, name_py, title, content)
                    print('%s %s 完成！' % (name, title))
    else:#不存在多个同名items
        page_url = 'https://baike.baidu.com/item/' + name
        list_url = urllib.parse.quote(page_url, safe='/:?=&')
        title, content = get_baidu_content_with_url(list_url)
        print(title,content[0:20])
        if title:
            send_contents_to_db(name, name_py, title, content)
            print('%s %s 完成！' % (name, title))
    return title,content
##############################name to baiduinfo end###############################################
def remove_patterns(text):
    pattern = r'\[\d+(-\d+)?\]'
    text = re.sub(pattern, '', text)
    return text

def add_keypeople(name):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    name_list=[]
    a = "select name from %s;" % (boss_db_table)
    cs.execute(a)
    people_list = cs.fetchall()
    for i in people_list:
        name_list.append(i[0])
    # print(name_list)
    if name not in name_list:
        title,content=get_person_4_details_to_db(name)
        if title=='':
            message="【%s】没有可用信息,不予建立"%(name)
        else:
            message="【%s】信息行建立成功"%(name)
            with open(txt_filename, 'r+') as file:
                # 读取文件内容
                content = file.readlines()
                # 在列表的第一个位置插入新的文本行
                content.insert(0, "%s\n"%(name))
                # 将光标移动到文件开头
                file.seek(0)
                # 将修改后的内容写回文件
                file.writelines(content)
        print(message)
        return message
    else:
        message = "【%s】信息行已存在" % (name)
        print(message)
        return message
# insert_keypeople('李强000')

#-姓名
def del_people(name):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    a = "select name from %s;" % (boss_db_table)
    cs.execute(a)
    name_list = cs.fetchall()
    # print(code)
    # print(code_list)
    namelist=[]
    for i in name_list:
        namelist.append(i[0])
    # print(codelist)
    if name in namelist:
        t = """DELETE FROM %s WHERE name='%s';""" % (boss_db_table, name)
        try:
            cs.execute(t)
            conn.commit()
            conn.close()
            message = "【%s】信息行删除成功" % (name)
            ###########删除名称后更新txt文件###############
            with open(txt_filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            # 过滤掉与目标姓名相同的行
            updated_lines = [line for line in lines if line.strip() != name]
            # 将过滤后的内容写回文件
            with open(txt_filename, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)
            print(message)
        except sqlite3.Error as e:
            message = "删除错误，无法执行删除操作"
            print(message)
    else:
        conn.close()
        message = "姓名不在数据库中"
        print(message)
    return message

#@姓名
def reply_name(name):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    tab_name = []
    a = "select name from %s;"%(boss_db_table)
    cs.execute(a)
    tab_list = cs.fetchall()
    for i in tab_list:
        tab_name.append(i[0])
    # print(tab_list)
    if name in tab_name:
        t= "select * from %s where name='%s';"%(boss_db_table,name)
        cs.execute(t)
        tab_list = cs.fetchall()
        cs.close()
        conn.commit()
        conn.close()
        if len(tab_list)==1:
            message0 = tab_list[0]
            code = message0[0]
            name = message0[1]
            title = message0[3]
            content = message0[4]
            other = message0[5]
            message = """%s - %s\n职务：%s \n经历：%s \n其他：%s""" % (name, code, title, content, other)
            print(message[0:20])
            return message
        else:
            code_name_list = []
            message =''
            for l in tab_list:
                message0 = l
                code = message0[0]
                title = message0[3]
                code_name_list.append([code,title])
                message += '%s %s\n'%(code,title)
            message=message[0:-1]
                # message = """【%s】- %s\n职务：%s""" % (name, code, title)
            print(message[0:20])
            return message
    else:
        cs.close()
        conn.commit()
        conn.close()
        message="请先新建【%s】档案"%(name)
        print(message)
        return message
#@py
def reply_py(py):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    tab_py = []
    a = "select name_py from %s;"%(boss_db_table)
    cs.execute(a)
    tab_list = cs.fetchall()
    for i in tab_list:
        tab_py.append(i[0])
    # print(tab_py)
    if py in tab_py:
        t= "select * from %s where name_py='%s';"%(boss_db_table,py)
        # print(t)
        cs.execute(t)
        tab_list = cs.fetchall()
        cs.close()
        conn.commit()
        conn.close()
        # print(len(tab_list))
        if len(tab_list)==1:
            message0 = tab_list[0]
            code = message0[0]
            name = message0[1]
            title = message0[3]
            content = message0[4]
            other = message0[5]
            message = """%s - %s\n职务：%s \n经历：%s \n其他：%s""" % (name, code, title, content, other)
            print(message[0:20])
            return message
        else:
            code_name_list = []
            message =''
            for l in tab_list:
                message0 = l
                code = message0[0]
                name=message0[1]
                title = message0[3]
                code_name_list.append([code,name,title])
                message += '%s %s %s\n'%(code,name,title)
            message = message[0:-1]
                # message = """【%s】- %s\n职务：%s""" % (name, code, title)
            print(message[0:20])
            return message
    else:
        cs.close()
        conn.commit()
        conn.close()
        message="请先新建【%s】档案"%(py)
        print(message)
        return message

#@code
def reply_code(code):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    a = "select * from %s where code='%s';"%(boss_db_table,code)
    cs.execute(a)
    tab_list = cs.fetchall()
    cs.close()
    conn.commit()
    conn.close()
    if len(tab_list)>0:
        message0 = tab_list[0]
        code = message0[0]
        name = message0[1]
        title = message0[3]
        content = message0[4]
        other = message0[5]
        message = """%s - %s\n职务：%s \n经历：%s \n其他：%s""" % (name, code, title, content, other)
        print(message[0:20])
        return message

    else:
        message="请先新建【%s】档案"%(code)
        print(message)
        return message
# reply_code('20681')

#title关键字 查询title内容
def search_title(title):
    boss_db_table = 'contentlist'
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    a1 = """select code,name,title from %s where title like """ %(boss_db_table)
    a2="'%"
    a3= "%';"
    a= a1+a2+title+a3
    # print(a)
    cs.execute(a)
    message = cs.fetchall()
    if len(message)==0:
        message='空'
        print(message)
        return message
    else:
        message0=''
        for i in message:
            message0+="""%s,%s,%s\n"""%(i[0],i[1],i[2])
        message0 = message0[0:-1]
        print(message0[0:20])
        return message0
# search_title('中央政治局常委')

#content关键字 查询content内容
def search_content(content):
    boss_db_table = 'contentlist'
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    a1 = """select code,name,title from %s where content like """ %(boss_db_table)
    a2="'%"
    a3= "%';"
    a= a1+a2+content+a3
    # print(a)
    cs.execute(a)
    message = cs.fetchall()
    if len(message)==0:
        message='空'
        print(message)
        return message
    else:
        message0=''
        for i in message:
            message0+="""%s,%s,%s\n"""%(i[0],i[1],i[2])
        message0 = message0[0:-1]
        print(message0[0:20])
        return message0
# search_content('山东农业大学植保系植保专业学习')

#s关键字&关键字 查询经历内容
def search_2(content,content1):
    boss_db_table = 'contentlist'
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    a1 = """select code,name,title from %s where content like """ %(boss_db_table)
    a2="'%"
    a3=" and content like '"
    a4= "%';"
    a= a1+a2+content+'%\''+a3+'%'+content1+a4
    # select 姓名,任职省,职务,经历 from boss_db_table where 经历 like  '% and 经历 like ' %';
    # print(a)
    cs.execute(a)
    message = cs.fetchall()
    if len(message)==0:
        message='空'
        print(message)
        return message
    else:
        message0 = ''
        for i in message:
            message0 += """%s,%s,%s\n""" % (i[0], i[1], i[2])
        message0=message0[0:-1]
        print(message0[0:20])
        return message0
# search_2('海南','浙江')

#s关键字&关键字 查询经历内容
def search_3(content,content1,content2):
    boss_db_table = 'contentlist'
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    a1 = """select code,name,title from %s where content like """ %(boss_db_table)
    a2="'%"
    a3=" and content like '"
    a4= "%'"
    a5 = " and content like '%"
    a6 = "%';"
    a= a1+a2+content+'%\''+a3+'%'+content1+a4+a5+content2+a6
    # select 姓名,任职省,职务,经历 from boss_db_table where 经历 like '%内容1%' and 经历 like '%content%' and 经历 like '%content%';
    # print(a)
    cs.execute(a)
    message = cs.fetchall()
    if len(message)==0:
        message='空'
        print(message)
        return message
    else:
        message0 = ''
        for i in message:
            message0 += """%s,%s,%s\n""" % (i[0], i[1], i[2])
        message0 = message0[0:-1]
        print(message0[0:20])
        return message0

###############################################todo程序部分###############################################
def get_list(db_table):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT id,content FROM '%s';""" % (db_table)
    cs.execute(t)
    data = cs.fetchall()
    list_content = '\n'.join([f'{row[0]}. {row[1]}' for row in data])
    print(list_content)
    conn.commit()
    conn.close()
    return list_content
def add_list(content,db_table):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    t = "INSERT OR IGNORE INTO {} ('content') VALUES (?)".format(db_table)
    cs.execute(t,(content,))
    conn.commit()
    conn.close()
def del_list(the_id,db_table):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    t = """DELETE FROM %s WHERE id='%s';""" % (db_table, the_id)
    cs.execute(t)
    conn.commit()
    conn.close()
def check_renew_list(db_table):
    conn = sqlite3.connect(db_name)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT content FROM '%s';""" % (db_table)
    cs.execute(t)
    list0=cs.fetchall()
    cs.close()
    conn.close()
    if len(list0)>0:
        return 1
    else:#表格为空
        return 0
def renew_list(db_table):
    conn = sqlite3.connect(db_name)
    css = conn.cursor()
    t="""delete from sqlite_sequence where name = '%s';"""%(db_table)
    print(t)
    css.execute(t)
    conn.commit()
    css.close()
    conn.close()


@bot.listener.on_message_event
async def echo(room, event):
    match = botlib.MessageMatch(room, event, bot)
    if match.is_not_from_this_bot() and match.is_from_allowed_user():
    # if match.is_not_from_this_bot():
        args=event.body
        thekey=args[0]
        # message=''
        if thekey=='+':
            thecontent=args[1:]
            if all('\u4e00' <= c <= '\u9fff' for c in thecontent):
                message=add_keypeople(thecontent)
                await bot.api.send_text_message(room.room_id,message)
                message1=reply_name(thecontent)
                message2 = remove_patterns(message1)
                await bot.api.send_text_message(room.room_id, message2)
            else:
                message = '输入的不是有效姓名'
                await bot.api.send_text_message(room.room_id, message)
        elif thekey=='-':
            name = args[1:]
            message = del_people(name)
            await bot.api.send_text_message(room.room_id, message)

        elif thekey=='@':
            thecontent0 = args[1:]
            # 检查是否是数字
            if thecontent0.isdigit():
                code=str(thecontent0)
                message0 =reply_code(code)
                message=remove_patterns(message0)
                await bot.api.send_text_message(room.room_id,message)
            #检查是否是拼音
            elif all('\u0041' <= c <= '\u005a' or '\u0061' <= c <= '\u007a' for c in thecontent0):
                # print('isalpha')
                code=str(thecontent0)
                message0 =reply_py(code)
                message=remove_patterns(message0)
                text_length = len(message)
                chunk_size=2000
                # 按照chunk_size分割文本
                chunks = [message[i:i + chunk_size] for i in range(0, text_length, chunk_size)]
                for ch in chunks:
                    await bot.api.send_text_message(room.room_id, ch)
            # 检查是否是汉字
            elif all('\u4e00' <= c <= '\u9fff' for c in thecontent0):
                name=thecontent0
                message0 =reply_name(name)
                message=remove_patterns(message0)
                await bot.api.send_text_message(room.room_id,message)
            else:
                message='输入了错误字符！'
                await bot.api.send_text_message(room.room_id, message)
        elif thekey=='z':
            thecontent0 = args[1:]
            message=search_title(thecontent0)
            await bot.api.send_text_message(room.room_id,message)
        elif thekey=='s':
            thecontent0 = args[1:]
            parts = thecontent0.split('&')
            if len(parts) == 2:
                content = parts[0]
                content1 = parts[1]
                message = search_2(content, content1)
                await bot.api.send_text_message(room.room_id,message)
            #con1&con2&con3
            elif len(parts) == 3:
                content = parts[0]
                content1 = parts[1]
                content2=parts[2]
                message = search_3(content, content1,content2)
                await bot.api.send_text_message(room.room_id,message)
            else:
                message = search_content(thecontent0)
                await bot.api.send_text_message(room.room_id, message)
        elif 'todo' == args[0:4]:
            if 'todo' == args:
                message0 = get_list(todo_db_table)
                if len(message0) == 0:
                    message = '空'
                else:
                    message = 'todo：'+'\n'+message0
                print(message)
                await bot.api.send_text_message(room.room_id, message)
                print('todolist')
            elif '+' == args[4]:
                thel = args[5:]
                add_list(thel,todo_db_table)
                message = get_list(todo_db_table)
                message='todo：'+'\n'+message
                print(message)
                await bot.api.send_text_message(room.room_id, message)
                print('list+内容1 完成')
            elif '-' == args[4]:
                the_id = args[5:]
                if the_id.isdigit():
                    del_list(the_id,todo_db_table)
                    if check_renew_list(todo_db_table)==0:
                        renew_list(todo_db_table)
                    message = get_list(todo_db_table)
                    message = 'todo：' + '\n' + message
                    await bot.api.send_text_message(room.room_id, message)
                    print(message)
                else:
                    message = '输入id错误'
                    message = 'todo：' + '\n' + message
                    print(message)
                    await bot.api.send_text_message(room.room_id, message)
                print('todo-id 完成')
            else:
                message='todo error'
                await bot.api.send_text_message(room.room_id, message)
                print('todo error')
        elif 'Todo' == args[0:4]:
            if 'Todo' == args:
                message0 = get_list(Todo1_db_table)
                if len(message0) == 0:
                    message = '空'
                else:
                    message = 'Todo：'+'\n'+message0
                print(message)
                await bot.api.send_text_message(room.room_id, message)
                print('Todolist')
            elif '+' == args[4]:
                thel = args[5:]
                add_list(thel,Todo1_db_table)
                message = get_list(Todo1_db_table)
                message='Todo：'+'\n'+message
                print(message)
                await bot.api.send_text_message(room.room_id, message)
                print('Llist+内容1 完成')
            elif '-' == args[4]:
                the_id = args[5:]
                if the_id.isdigit():
                    del_list(the_id,Todo1_db_table)
                    if check_renew_list(Todo1_db_table)==0:
                        renew_list(Todo1_db_table)
                    message = get_list(Todo1_db_table)
                    message = 'Todo：' + '\n' + message
                    await bot.api.send_text_message(room.room_id, message)
                    print(message)
                else:
                    message = '输入id错误'
                    message = 'Todo：' + '\n' + message
                    print(message)
                    await bot.api.send_text_message(room.room_id, message)
                print('Todo-id 完成')
            else:
                message='Todo error'
                await bot.api.send_text_message(room.room_id, message)
                print('Todo error')
        elif args == 'h':
            message = '指令格式：\n@姓名：精确查询某人信息，重名返回列表\n@py：拼音首字母模糊查询，重名返回列表\n@123：根据编号精确查询\n+姓名：新增某人信息\n-姓名：删除所有该姓名的信息\nz职务：根据职务关键字查询\ns内容：根据主要经历关键字查询\ns内容&内容&内容：根据3个关键字查询\ntodo：todo/Todo,todo+内容,todo-id'

            await bot.api.send_text_message(room.room_id,message)
        else:
            message = 'error'
            await bot.api.send_text_message(room.room_id, message)

# 使用 asyncio 的事件循环来运行 bot.run()
loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run())
