from flask import Flask, request
import threading
import queue
import requests
import json
import os
import mimetypes

# 创建 magic 实例并打开默认数据库

app = Flask(__name__)
msg_queue = queue.Queue()
mirai_server="http://127.0.0.1:9551/"
langchain_tigerbot_server="http://127.0.0.1:7861/"
#本地知识默认为关闭状态，可以通过群里@机器人 开启知识库 方式打开，或者直接将该值改为False
local_doc_qa_off=True


#获取授权
def gettoken(qq=''):
    url = mirai_server+'verify'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {'verifyKey': 'INITKEY51FSDeVs'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code) 
    print(response.text)
    response_data = response.json()
    if response_data['code']==0:
        session=response_data['session']
        print(session)
        data={"sessionKey":session,"qq":int(qq)}
        url = mirai_server+'bind'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code) 
        print(response.text)
        response_data = response.json()
        if response_data['code']==0:
            return session


   
    return ''


#解除授权
def releasetoken(qq=0,session=''):
    url = mirai_server+'release'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {'sessionKey': session,'qq':qq}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code) 
    print(response.text)

#发送群消息 
def sendmsg(group='',session='',answer=''):
    if not group or not answer or not session:
        return
    url = mirai_server+'sendGroupMessage'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {'sessionKey': session,'target':int(group),"messageChain":[{"type":"Plain","text":answer}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code) 
    print(response.text)

#获取当前文件地址 
def getfileurl(group='',id='',session='',filename=''):
    if not group or not id or not session:
        return
    url = mirai_server+'file/info?sessionKey='+session+'&id='+str(id)+'&target='+str(group)+'&withDownloadInfo=true'
    response = requests.get(url)
    # 检查响应状态码是否为 200，表示请求成功
    if response.status_code == 200:
        # 获取 JSON 响应内容，并将其解析为 Python 字典类型
        json_data = response.json()
        # 打印 JSON 数据
        print(json_data)
        if json_data.get('code')==0:
            fileurl=json_data['data']['downloadInfo']['url']
            re=upload_file(fileurl,group,filename)
            if re==1:
                return 'ok'
            else:
                return
                
    else:
        print(f"请求失败，状态码为 {response.status_code}")
        return
    return

#上传文件到知识库
def upload_file(url='',group='',filename=''):
    print(url)
    print(group)
    print(filename)
    # Download the file
    response = requests.get(url)
    # Determine the file's MIME type
    content_type = response.headers['Content-Type']
    file_type, encoding = mimetypes.guess_type(filename)
    if not file_type:
        file_type = content_type.split(';')[0]
    print(file_type)
    # Upload the file
    url = langchain_tigerbot_server+'local_doc_qa/upload_files'
    headers = {'accept': 'application/json'}
    files = {'files': (filename, response.content, file_type)}
    data = {'knowledge_base_id': str(group)}
    response = requests.post(url, headers=headers, files=files, data=data)
    rejson=response.json()
    if rejson['code']==200:
        return 1
    return 0

#通过群id获取知识库文件列表
def list_files(group=''):
    url = langchain_tigerbot_server+'local_doc_qa/list_files?knowledge_base_id='+str(group)
    re=''
    response = requests.get(url)
    if response.status_code == 200:
        # 获取 JSON 响应内容，并将其解析为 Python 字典类型
        json_data = response.json()
        re = "\n".join(json_data["data"])
    return re

#删除知识库中的文件
def del_files(group='',filename=''):
    url = langchain_tigerbot_server+'local_doc_qa/delete_file'
    params = {
        'knowledge_base_id': group,
        'doc_name': filename
    }
    headers = {
        'accept': 'application/json'
    }

    response = requests.delete(url, params=params, headers=headers)

    if response.ok:
        print('文件删除成功')
        return 1
    else:
        print('文件删除失败，HTTP状态码：', response.status_code)
    return 0

#从知识库获取答案
def generate(question="",knowledge_base_id=""):
    if not question:
        return "您提交了一个空问题，无法解答。"
    url=""
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if local_doc_qa_off:
        url = langchain_tigerbot_server+'chat'
        data = {"question": question,"history": []}
    else:
        url = langchain_tigerbot_server+'local_doc_qa/local_doc_chat'
        data = {"knowledge_base_id":knowledge_base_id,"question": question,"history": []}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code) 
    print(response.text)
    response_data = response.json()
    answer=response_data['response']
    return answer

# 启动一个线程，每次处理队列中的第一条数据，并移除第一条
def print_msg():
    global local_doc_qa_off
    global local_doc_group
    while True:
        if not msg_queue.empty():
            msg = msg_queue.get()
            msgjson=json.loads(msg)
            print(msgjson)
            #申请操作session
            session=gettoken(msgjson['qq'])
            if msgjson['type']=='GroupMessage':
                data=msgjson['messageChain']
                At=False
                msgtxt=""
                group=msgjson['sender']['group']['id']
                senduser=msgjson['sender']['memberName']
                for item in data:
                    print(item.get("type"))
                    print(item.get('target'))
                    # 如果这个元素是 "at" 类型，且对象是qq机器人自己则触发问答
                    if item.get("type") == "At" and item.get('target')==int(msgjson['qq']):
                        print(item.get("target"))
                        At=True
                    elif item.get("type")=="Plain":
                        msgtxt=item.get("text")
                        msgtxt=msgtxt.strip()
                    elif item.get("type")=='File':
                        filename=item.get("name")
                        extension = os.path.splitext(filename)[1]
                        extension=extension.lower()
                        print(filename)
                        if extension=='.pdf' or extension==".txt" or extension==".docx" or extension==".md":
                            id=item.get("id")
                            re=getfileurl(group,id,session,filename)
                            if re=="ok":
                                answer="@"+senduser+" 知识库文件："+filename+" 已成功加载，请切换到知识库模式便可提问。"
                            else:
                                answer="@"+senduser+" 知识库文件："+filename+" 加载失败！"
                        print(answer)
                        sendmsg(group,session,answer)


                if At:
                    if msgtxt=='关闭知识库':
                        local_doc_qa_off=True
                        answer="@"+senduser+" 知识库模式已关闭！"
                    elif msgtxt=="开启知识库":
                        local_doc_qa_off=False
                        answer="@"+senduser+" 知识库模式已开启！"
                    elif msgtxt=="查看知识库":
                        local_doc=list_files(group)
                        answer="@"+senduser+" 当前知识库文件：\r"+local_doc
                    elif msgtxt.startswith("删除文件"):
                        remaining_txt = msgtxt[len("删除文件"):].strip()
                        re=del_files(group,remaining_txt)
                        if re==1:
                            answer="@"+senduser+" 当前知识库文件："+remaining_txt+" 已删除！"
                        else:
                            answer="@"+senduser+" 当前知识库文件："+remaining_txt+" 删除失败！"
                    elif msgtxt=="info":
                        if local_doc_qa_off:
                            infotxt="知识库模式：已关闭"
                        else:
                            infotxt="知识库模式：已开启"
                        answer="@"+senduser+"\r"+infotxt
                    else:
                        answer="@"+senduser+" "+generate(msgtxt,group)
                    
                    print(answer)
                    sendmsg(group,session,answer)
            #用完必须要回收
            releasetoken(int(msgjson['qq']),session)








thread = threading.Thread(target=print_msg)
thread.daemon = True
thread.start()

# 接收post请求，将数据保存到队列中
@app.route('/msg', methods=['POST'])
def save_msg():
    msg = request.json
    qq=request.headers.get('qq')
    if not qq:
        qq = request.headers.get('bot')
    if not qq:
        qq = request.headers.get('X-qq')
    if not qq:
        qq = request.headers.get('X-bot')

    if qq:
        msg['qq'] = qq

    msg_queue.put(json.dumps(msg))
    return 'OK'

if __name__ == '__main__':
    app.run(port=9550)