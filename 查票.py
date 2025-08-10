import os
import re
import requests
import json
import time
import datetime
from pygame import mixer
from rich import progress
import rich
from rich import status

mixer.init()

########## Program Config

SLEEP_TIME = 30

########## Train Information

LEAVE_DATE = YEAR, MONTH, DAY = 2025, 7, 30

FROM = 'NXG' # 南昌西
TO = 'XBG' # 新余北

TRAIN = 'G2413'

TYPE = {
    '二等座': 30
}['二等座']

AMOUNT = 3

########## Program

url = "https://kyfw.12306.cn/otn/leftTicket/queryU"

querystring = {"leftTicketDTO.train_date": f"{YEAR}-{MONTH}-{DAY}", "leftTicketDTO.from_station": FROM,
               "leftTicketDTO.to_station": TO, "purpose_codes": "ADULT"}

headers = {
    "Host": "kyfw.12306.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "If-Modified-Since": "0",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    # "Referer": "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8D%97%E6%98%8C%E8%A5%BF,NXG&ts=%E6%96%B0%E4%BD%99%E5%8C%97,XBG&date=2025-07-17&flag=N,N,Y",
    "Cookie": "_jc_save_toDate=",
    # "Cookie": "_uab_collina=169052744831903315656823; JSESSIONID=B2E9D933B68DD9BDE990299F6C658646; BIGipServerotn=1893269770.24610.0000; BIGipServerpassport=786956554.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; fo=vw456bhkx2yp7lvlO3DCwWJFCKFyDuZyTnDrciGa7gnz2wLMY1l2rRISl93ZKOSSKeAa-G6qWFUM89PDVA9zxZf5Lq6ap-8p-KNZ9xLn9-zwTytUQpIVb5shE2LihHGR1EXOn79X2XRNo2eZVLWBP9L46QvD_PEUyMYDR8sX5IgjVOCc7F5NOJgy4eQ; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromStation=%u592A%u539F%2CTYV; _jc_save_toStation=%u5357%u660C%2CNCG; _jc_save_fromDate=2023-08-07; _jc_save_toDate=2023-07-28; _jc_save_wfdc_flag=dc",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

def do_query():
    dt = datetime.date.today()
    while dt <= datetime.date(*LEAVE_DATE):
        qs = querystring | {"leftTicketDTO.train_date": f"{YEAR}-{dt.month:02}-{dt.day:02}"}
        response = requests.request("GET", url, headers=headers, params=qs)
        data = json.loads(response.text)
        if data["httpstatus"] == 200 and TRAIN in response.text:
            yield (dt.month, dt.day), data["data"]["result"]
        dt += datetime.timedelta(1)

def is_enough(x):
    return x == '有' or (x.isdigit() and int(x) >= AMOUNT)

lstt = None
if os.path.exists('record.txt'):
    with open('record.txt') as f:
        op2 = []
        for r in re.split(r' +', f.read().strip('\n').split('\n')[-1].strip()):
            tmp = 'green' if is_enough(r) else 'red'
            pr = r.ljust(7) if r in ("有", "无") else r.ljust(8)
            op2.append(f"[{tmp}]{pr}[/{tmp}]")
        lstt = op2
with progress.Progress() as pg:
    while True:
        st = time.time()
        qtsk = pg.add_task("正在查询……", total=None)
        result = do_query()
        result = [(d, list(filter(lambda x: x[3] == TRAIN, map(lambda x: x.split('|'), r)))[0][TYPE]) for d, r in result]
        fnr = list(filter(lambda x: x[0] == (MONTH, DAY), result))[0][1]
        op1 = []
        op2 = []
        for d, r in result:
            op1.append(f'{d[0]:02}-{d[1]:02}')
            tmp = 'green' if is_enough(r) else 'red'
            pr = r.ljust(7) if r in ("有", "无") else r.ljust(8)
            op2.append(f"[{tmp}]{pr}[/{tmp}]")
        if lstt and lstt != op2:
            with open('record.txt', 'a') as f:
                f.write(time.strftime("[%m-%d %H:%M:%S]", time.localtime())+"\n")
                f.write('   '.join(op1)+"\n")
                f.write(re.sub(r'\[.*?\]', '', ''.join(op2))+"\n\n")
        lstt = op2
        pg.remove_task(qtsk)
        if is_enough(fnr):
            rich.print(f'[green]{time.strftime("[%m-%d %H:%M:%S]", time.localtime())}[/green]')
            rich.print('   '.join(op1))
            rich.print(''.join(op2))
            mixer.music.load(r'D:\温予乐\我的桌面\sl\新课程表\hkd\ngm-15-19.mp3')
            mixer.music.play(loops=5)
        else:
            rich.print(f'[red]{time.strftime("[%m-%d %H:%M:%S]", time.localtime())}[/red]')
            rich.print('   '.join(op1))
            rich.print(''.join(op2))
        rich.print()
        tsk = pg.add_task(f'{SLEEP_TIME}秒查询一次，请等待……', total=SLEEP_TIME)
        lst = st
        while time.time() < st + SLEEP_TIME:
            tmpt = time.time()
            pg.advance(tsk, tmpt-lst)
            lst = tmpt
            time.sleep(0.01)
        pg.remove_task(tsk)
