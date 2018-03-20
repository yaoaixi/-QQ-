#coding:utf-8
import json
import os
#获取好友QQ号码
def get_Frends_list():
    k = 0
    file_list=[i for i in os.listdir('./frends/') if i.endswith('json')]
    frends_list=[]
    for f in file_list:
        with open('./frends/{}'.format(f),'r',encoding='utf-8') as w:
            #data=w.read()[84:-470]#从哪里开始读取读取到哪里结束
            data = w.read()[84:-470]  # 从哪里开始读取读取到哪里结束
            print("ykk", data)
            js=json.loads(data)
            # print(js)
            for i in js:
                k+=1
                frends_list.append(i)
    return frends_list


frends_list=get_Frends_list()
#print(frends_list,"\n")
print ("获取成功！\n")