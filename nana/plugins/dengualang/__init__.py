#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/21 18:00:00
@Author  :   sdy623
@Contact :   a1470222899@live.cn
@Github  :   https://github.com/sdy623
@License :   MIT

'''
__author__ = 'sdy623'

import os
import json
import random
from pathlib import Path
from time import strftime
from zipfile import PyZipFile
from typing import Tuple, Dict, List
from datetime import datetime, timedelta
from nonebot import CommandSession, MessageSegment
from nonebot.plugin import on_command
from nonebot import on_natural_language, NLPSession, IntentCommand
#from utils.utils_banList import banList


file = Path('.') / 'nana' / 'data' / 'data_IDcard' / 'main.bin'

def infoID() -> Tuple[Dict[str, List[str]], Dict[str, str]]:
    with PyZipFile(os.path.abspath(file), "r") as zipFile:
        with zipFile.open("name.json", "r") as f:
            name = json.loads(f.read().decode())
        with zipFile.open("area.json", "r") as f:
            area = json.loads(f.read().decode())
    return name, area

NAME, AREA = infoID()

BIRTH_BEGIN = datetime(*[1980, 10, 10]) # type: ignore
BIRTH_END = datetime(*[2002, 10, 10]) # type: ignore

def numberID(area: int, sex: int, birth: int) -> str:
    def checkSum(fullCode: str) -> int or str:
        assert len(fullCode) == 17
        checkSum = sum(
            [((1 << (17 - i)) % 11) * int(fullCode[i]) for i in range(0, 17)]
        )
        checkDigit = (12 - (checkSum % 11)) % 11
        if checkDigit < 10:
            return checkDigit
        else:
            return "X"
    
    orderCode = str(random.randint(10, 99))
    sexCode = str(random.randrange(sex, 10, step=2))
    fullCode = str(area) + str(birth) + str(orderCode) + str(sexCode)
    fullCode += str(checkSum(fullCode))
    return fullCode


plugin_name = "one-key-adult"

KEYWORDS=['登gua郎', '转大人', '打25小时游戏']

@on_command('denggualang',
            aliases=['登gua郎', '转大人', '打25小时游戏',*KEYWORDS],
            only_to_me=False)
async def _(session: CommandSession):
    id_card_area = int(random.choice(list(AREA.keys())))
    id_card_area_name = AREA[str(id_card_area)]
    id_card_year_old = timedelta(days=random.randint(0, (BIRTH_END - BIRTH_BEGIN).days) + 1)
    id_card_birth_day = strftime("%Y%m%d", (BIRTH_BEGIN + id_card_year_old).timetuple())
    id_card_sex = random.choice([0, 1])
    id_card_name = random.choice(NAME[{0: "female", 1: "male"}[id_card_sex]])
    id_card_id = numberID(id_card_area, id_card_sex, id_card_birth_day)

    msg0 = "恭喜，你已经成大人了！\n"
    msg0 += "这是你一天25h游戏的通行证：\n"
    msg0 += f"NumberID: {id_card_id}\n"
    msg0 += f"Sex: {'男' if id_card_sex == 1 else '女'}\n"
    msg0 += f"Name: {id_card_name} || Address: {id_card_area_name}\n"
    msg0 += "注: 1、以上信息根据国家公开标准生成，非真实信息。\n"
    msg0 += "     2、不适用于网易和腾讯。"
    session.finish(msg0)

@on_natural_language(KEYWORDS)
async def _(session: NLPSession):
    miss = max(0, len(session.msg_text) - 4) * 5
    return IntentCommand(100.0 - miss, 'denggualang')