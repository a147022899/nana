import os
import re
import time
import json
import sqlite3
import requests
from urllib.parse import urlencode
from random import choice, randint
from pathlib import Path
from datetime import datetime
from random import choice
import nonebot
from nonebot import on_command, CommandSession

import config # type: ignore
from nana.modules.b64 import b64_str_img_url # type: ignore
from nana.modules.response import request_api_params # type: ignore
from nana.modules.funcControl import checkSwitch, checkNoob # type: ignore
from nonebot import on_natural_language, NLPSession, IntentCommand

bot = nonebot.get_bot()
master = bot.config.SUPERUSERS
apikey_LOLI = bot.config.LOLICONAPI
APP_ID = bot.config.BAIDU_AIP_APP_ID
API_KEY = bot.config.BAIDU_AIP_API_KEY
SECRECT_KEY = bot.config.BAIDU_AIP_SECRET_KEY
__plugin_name__ = "setu"
__plugin_name1__ = "setu_img"

URL = 'https://api.lolicon.app/setu/'

SETU_REPLY = """Title: {title}
Pid: {pid}
{setu}
---------------
Complete time:{time}s"""

KEYWORDS = ['涩色瑟', '搞快点', '色色', '涩涩', '瑟瑟', '福利', 'boki','色图','涩图']

def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now

#aliases = (r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]|[图圖]来|[我你她他它]想要[点丶张份副][涩色瑟][图圖]|我想要[1一][张份幅副个只][涩色瑟][图圖]|[我你她他它]想[看|look][涩涩|色色]的东西"),

setu_type = 1
@on_command('setu', aliases=['色图', '涩图', '图圖', *KEYWORDS],
            only_to_me=False)
async def setu(session: CommandSession):
    start = time.perf_counter()
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            await session.send(
                choice(
                    [
                        'zzzz......',
                        'zzzzzzzz......',
                        'zzz...好涩哦..zzz....',
                        '别...不要..zzz..那..zzz..',
                        '嘻嘻..zzz..呐~..zzzz..'
                    ]
                )
            )
        else:
            if checkSwitch(__plugin_name__):
                res = randint(1,10)
                if 1 <= res < 9:
                    res = randint(1,4)
                    if 1 <= res < 3:
                        if setu_type == 1:
                            res = randint(1,4)
                            await session.send('别急！正在找图！')
                            con = sqlite3.connect(Path('.') / 'nana' / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
                            cur = con.cursor()
                            msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')
                        
                            if 1 <= res < 3:
                                for i in msg:
                                    pid = i[0]
                                    title = i[1]
                                    img = i[7]
                                    end = time.perf_counter()
                                    await session.send(
                                        SETU_REPLY.format(
                                        title = title,
                                        pid = pid,
                                        setu = img,
                                        time = round(end - start, 3)
                                        )
                                    )
                            elif res == 4:
                                for i in msg:
                                    pid = i[0]
                                    title = i[1]
                                    img = i[7]
                                    end = time.perf_counter()
                                    await session.send('我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆')
                                    await bot.send_private_msg( # type: ignore
                                        user_id = master,
                                        message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{img}\nComplete time: {round(end - start, 3)}"
                                    )
                        
                        elif setu_type == 2:
                            res = randint(1,4)
                            await session.send('别急！正在找图！')
                            start = time.perf_counter()
                            values = {
                                "apikey": apikey_LOLI,
                                "r18": "0",
                                "num": "1"
                            }

                            try:
                                dc = json.loads(request_api_params(URL, values))
                                title = dc["data"][0]["title"]
                                pid = dc["data"][0]["pid"]
                                setu = dc["data"][0]["url"] #b64.b64_str_img_url(dc["data"][0]["url"])
                            except:
                                await session.send('失败了失败了失败了失...')
                                return
                            if 1 <= res < 3:
                                end = time.perf_counter()
                                await session.send(
                                    SETU_REPLY.format(
                                    title = title,
                                    pid = pid,
                                    setu = dc["data"][0]["url"],
                                    time = round(end - start, 3)
                                    )
                                )
                            elif res == 4:
                                end = time.perf_counter()
                                await session.send('我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆')
                                await bot.send_private_msg( # type: ignore
                                    user_id = master,
                                    message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{setu}\nComplete time: {round(end - start, 3)}"
                                )
                    elif res == 4:
                        img = choice(
                            [
                                'SP.jpg', 'SP1.jpg', 'SP2.jpg'
                            ]
                        )
                        img = Path('.') / 'nana' / 'data' / 'emoji' / f'{img}'
                        img = os.path.abspath(img)
                        await session.send(f'[CQ:image,file=file:///{img}]')
                
                elif res == 10:
                    img = choice(
                        [
                            'GDZ.png', 'SHZY1.jpg', 'SHZY2.jpg', 'SHZY3.jpg', 'SHZY4.jpg', 'SHZY5.jpg', 'SHZY6.jpg'
                        ]
                    )
                    img = Path('.') / 'nana' / 'data' / 'img' / 'niceIMG' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')

            else:
                await session.send('该功能已关闭...')


@on_command('change_setu_type', aliases = ['涩图导向'], only_to_me = False)
async def _(session: CommandSession):
    global setu_type
    if session.event.user_id == master:
        msg = session.event.raw_message.split(' ', 1)
        s_type = msg[1]
        
        if s_type == '数据库':
            setu_type = 1
        
        elif s_type == '接口':
            setu_type = 2
        
        else:
            pass
        
        await session.send('okay~~~~')


@bot.on_message("group")
async def _(context):
    start = time.perf_counter()
    user = context["user_id"]
    group = context["group_id"]
    if checkNoob(user, group):
            if checkSwitch(__plugin_name1__):
                try:
                    img = str(context["message"])
                    pattern = re.compile(r"url=(.*)]")
                    img = re.findall(pattern, img)
                    img = img[0].replace('url=', '')
                    img = img.replace(']', '')
                    print(img)
                except:
                    return

                img = b64_str_img_url(img)
                if img:
                    try:
                        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRECT_KEY}'
                        headers = {
                            'Content-Type': 'application/json;charset=UTF-8'
                        }
                        res = json.loads(request_api_params(host, headers))
                        access_token=res['access_token']
                        url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token={access_token}'
                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                        data = urlencode({'image': img})
                        res = requests.post(url=url, headers=headers, data=data)
                    except:
                        return
                    
                    try:
                        words = json.loads(res.content)['words_result'][0]['words']
                        print(words)
                    except:
                        return

                    if re.findall(r"[涩色]图|炼铜", words):
                        if checkSwitch(__plugin_name__):
                            res = randint(1,10)
                            if 1 <= res < 9:
                                res = randint(1,4)
                                if 1 <= res < 3:
                                    if setu_type == 1:
                                        res = randint(1,4)
                                        con = sqlite3.connect(Path('.') / 'nana' / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
                                        cur = con.cursor()
                                        msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')
                                    
                                        if 1 <= res < 3:
                                            for i in msg:
                                                pid = i[0]
                                                title = i[1]
                                                img = i[7]
                                                end = time.perf_counter()
                                                msg = SETU_REPLY.format(
                                                    title = title,
                                                    pid = pid,
                                                    setu = img,
                                                    time = round(end - start, 3)
                                                )
                                                await bot.send_group_msg(group_id = group, message = msg) # type: ignore
                                        elif res == 4:
                                            for i in msg:
                                                pid = i[0]
                                                title = i[1]
                                                img = i[7]
                                                end = time.perf_counter()
                                                await bot.send_group_msg(group_id = group, message = '我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆') # type: ignore
                                                await bot.send_private_msg( # type: ignore
                                                    user_id = master,
                                                    message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{img}\nComplete time: {round(end - start, 3)}"
                                                )
                                    
                                    elif setu_type == 2:
                                        res = randint(1,4)
                                        await bot.send_group_msg(group_id = group, message = '别急！正在找图！') # type: ignore
                                        start = time.perf_counter()
                                        values = {
                                            "apikey": apikey_LOLI,
                                            "r18": "0",
                                            "num": "1"
                                        }

                                        try:
                                            dc = json.loads(request_api_params(URL, values))
                                            title = dc["data"][0]["title"]
                                            pid = dc["data"][0]["pid"]
                                            setu = dc["data"][0]["url"] #b64.b64_str_img_url(dc["data"][0]["url"])
                                        except:
                                            await bot.send_group_msg(group_id = group, message = '失败了失败了失...') # type: ignore
                                            return
                                        if 1 <= res < 3:
                                            end = time.perf_counter()
                                            msg = SETU_REPLY.format(
                                                    title = title,
                                                    pid = pid,
                                                    setu = img,
                                                    time = round(end - start, 3)
                                                )
                                            await bot.send_group_msg(group_id = group, message = msg) # type: ignore
                                        elif res == 4:
                                            end = time.perf_counter()
                                            await bot.send_group_msg(group_id = group, message = '我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆') # type: ignore
                                            await bot.send_private_msg( # type: ignore
                                                user_id = master,
                                                message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{setu}\nComplete time: {round(end - start, 3)}"
                                            )
                                elif res == 4:
                                    img = choice(
                                        [
                                            'SP.jpg', 'SP1.jpg', 'SP2.jpg'
                                        ]
                                    )
                                    img = Path('.') / 'nana' / 'data' / 'emoji' / f'{img}'
                                    img = os.path.abspath(img)
                                    await bot.send_group_msg(group_id = group, message = f'[CQ:image,file=file:///{img}]') # type: ignore
                            
                            elif res == 10:
                                img = choice(
                                    [
                                        'GDZ.png', 'SHZY1.jpg', 'SHZY2.jpg', 'SHZY3.jpg', 'SHZY4.jpg', 'SHZY5.jpg', 'SHZY6.jpg'
                                    ]
                                )
                                img = Path('.') / 'nana' / 'data' / 'img' / 'niceIMG' / f'{img}'
                                img = os.path.abspath(img)
                                await bot.send_group_msg(group_id = group, message = f'[CQ:image,file=file:///{img}]') # type: ignore

                        else:
                            pass
            
            else:
                pass
@on_natural_language(KEYWORDS)
async def _(session: NLPSession):
    miss = max(0, len(session.msg_text) - 4) * 5
    return IntentCommand(100.0 - miss, 'setu')