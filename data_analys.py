import json
import os
import xlwt
import time
import pymysql
#数据存入Excel以及数据库

def dataToExcel():
    ll=1
    d=[i for i in os.listdir('mood_detail') if not i.endswith('.xls')]
    for ii in d:
        wb=xlwt.Workbook()
        sheet=wb.add_sheet('sheet1',cell_overwrite_ok=True)
        sheet.write(0,0,'content')
        sheet.write(0,1,'createTime')
        sheet.write(0,2,'source_name')
        sheet.write(0,3,'cmtnum')
        fl=[i for i in os.listdir('mood_detail/'+ii) if i.endswith('.json')]
        print('mood_detail/'+ii)
        k=1
        for i in fl:
            with open('mood_detail/'+ii+"/"+i,'r',encoding='utf8') as w:
                s=w.read()[17:-2]
                #print (s)
                js=json.loads(s)
                print(i)
                for s in js['msglist']:
                    ll+=1
                    m=-1
                    img=""
                    if 'pic' in s.keys():
                        for g in list(s['pic']):
                            img+=g['url1']+"\n"
                        sheet.write(k,m+1,str(s['content']+img))
                    else:
                        sheet.write(k, m + 1, str(s['content']))
                    sheet.write( k,m+2,str( time.strftime( "%Y-%m-%d %H:%M:%S",time.localtime(s['created_time']) ) ) )
                    sheet.write(k,m+3,str(s['source_name']))
                    sheet.write(k,m+4,str(s['cmtnum']))
                    k+=1
        if not os.path.exists('mood_detail/Excel/'):
            os.mkdir('mood_detail/Excel/')
        print("共计",ll,"条说说\n")
        try:
             wb.save('mood_detail/Excel/'+ii+'.xls')
        except Exception:
            print("error")

dataToExcel()





#存入数据库
def dataToMySql():
    con=pymysql.connect(
        host='localhost',
        user='root',
        password="yao951012",
        database='qzone_data',
        charset='utf8mb4'
    )
    cursor=con.cursor()
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')
    sql="insert into mood (qq_number,created_time,content,source_name,cmtnum,name) values (\"{}\",\"{}\",\"{}\",\"{}\",{},\"{}\");"

    d=[i for i in os.listdir('mood_detail') if not i.endswith('.xls')]
    for ii in d:
        fl=[i for i in os.listdir('mood_detail/'+ii) if i.endswith('.json')]
        print('mood_detail/'+ii)
        k=1
        for i in fl:
            with open('mood_detail/'+ii+"/"+i,'r',encoding='utf8') as w:
                s=w.read()[17:-2]
                js=json.loads(s)
                print(i)
                for s in js['msglist']:
                    if s['source_name']=="":
                        s['source_name']="未显示"
                    img = ""

                    if 'rt_uinname' in s.keys():
                        mcontents = str(s['content'])+'转发：'+s['rt_uinname']
                        if 'pic' in s.keys():
                            for g in list(s['pic']):
                                img += g['url1'] + "\n"
                            mcontents = str(s['content'] + img)
                        if 'video' in s.keys():
                            for g in list(s['video']):
                                img += '\n预览图：'+g['url1'] + "\n"+'视频：'+g['url3'] + "\n"
                            mcontents = str(s['content'] + img)
                    else:
                        if 'pic' in s.keys():
                            for g in list(s['pic']):
                                img += g['url1'] + "\n"
                            mcontents = str(s['content'] + img)
                        else:
                            mcontents = str(s['content'])
                    print (mcontents.replace('\u0022' ,'' ,2),str(s['source_name']))
                    print(sql.format(s['uin'], time.strftime( "%Y-%m-%d %H:%M:%S",time.localtime(s['created_time'])), s['content'], s['source_name'], int(s['cmtnum']),s['name']))
                    cursor.execute(sql.format(s['uin'],time.strftime( "%Y-%m-%d %H:%M:%S",time.localtime(s['created_time'])),mcontents.replace('"' ,'').replace('\\','\\\\'),str(s['source_name']),int(s['cmtnum']),str(s['name'])))
                    k+=1
    con.commit()
    con.close()

dataToMySql()