import requests
import json
buyred= [['02','24','10','18','20'],
         ['08','24','21','18','20'],
         ['08','24','10','21','20'],
         ['08','24','10','18','21'],
         ['05','11','28','31','35'],
         ['01','18','21','24','25'],
         ['01','08','09','14','27'],
         ['02','03','07','11','25']]
buyblue=[['04','09'],
         ['05','10'],
         ['06','11'],
         ['08','10'],
         ['05','07']]
zjjs=[[3,0,'5元'],
      [2,1,'5元'],
      [1,2,'5元'],
      [0,2,'5元'],
      [3,1,'15元'],
      [2,2,'15元'],
      [4,0,'100元'],
      [3,2,'200元'],
      [4,1,'300元'],
      [4,2,'3000元'],
      [5,0,'10000元'],
      [5,1,'10万元'],
      [5,2,'500万元']]
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
r = requests.get('https://webapi.sporttery.cn/gateway/lottery/getDigitalDrawInfoV1.qry?param=85,0&isVerify=1', headers=headers)
#r.encoding = 'gb2312'
json_data = json.loads(r.text)
jsd=json_data['value']['dlt']['lotteryDrawResult']
newjsd=jsd.split()
qianqu=newjsd[0:5]
houqu=newjsd[5:7]

#计算命中数
def zjcx(qianqu,houqu,buyred,buyblue):
    zjlist = []
    qiansum = 0
    housum = 0
    # 计算前区命中数
    for x in qianqu:
        for y in buyred:
            if x == y:
                qiansum = qiansum+1
#计算后区命中数
    for x in houqu:
        for y in buyblue:
            if x == y:
                housum = housum+1
    zjlist.append(qiansum)
    zjlist.append(housum)
    return zjlist
#返回命中数结果
listsums = []
i=0
while i < 8:
    if i<=3:
        oo=zjcx(qianqu,houqu,buyred[i],buyblue[0])
        listsums.append(oo)
        i = i+1
    elif i>3:
        oo = zjcx(qianqu, houqu, buyred[i], buyblue[i-3])
        listsums.append(oo)
        i = i + 1


desptext = []
sumss = 0
for exce in listsums:
    sumg = 0
    for its in zjjs:
        sumg=sumg+1
        if exce[0] == its[0] and exce[1] == its[1]:
            desptext.append(its[2])
            break
        elif sumg == 12:
            desptext.append('0元')
desp_text = '<ul>'
sum_text = 0
while sum_text < 8:
    xx=str(listsums[sum_text])
    yy = str(desptext[sum_text])
    str_text = '<li>'+str(sum_text+1)+'.'+xx+'--'+yy+'</li>\n'
    desp_text = desp_text+str_text
    sum_text=sum_text+1
desp_text = desp_text+'</ul>'
# soup = bs4.BeautifulSoup(r.text, 'html.parser')
# targets = soup.find_all("div", class_="ball_box01")
# for ech in targets:
#     print(ech.text)
datas = {'title':'【'+json_data['value']['dlt']['lotteryDrawTime']+'】','desp':jsd+'\n'+desp_text,'headers':headers}
r = requests.post('https://sctapi.ftqq.com/SCT48186TAsijecOtfjmuXLGHk2L2PhOK.send', data=datas)
print(r.status_code)