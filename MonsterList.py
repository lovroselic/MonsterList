# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 09:20:45 2021

@author: lovro selic
@version 0.1.0

private tool for creation of excel files from monster
definition in MAP module of CrawlMaster game
"""

import regex as re
import pandas as pd
from pandas import ExcelWriter
from collections import defaultdict

_file = "Monsters.js"
with open(_file) as fh:
    data = fh.read()

firstPattern = re.compile(r'var MONSTER\s*=\s*{[.\s\w\:{\"\',()}\[\]\-\/]*};')
monsters = re.search(firstPattern, data).group(0)
monsterExtractionPattern = re.compile(
    r'(\w+\:\s{[\s\w\:\"\,\.\(\)\[\]\-\/\']*})')
test = re.compile(r'magic')
attributePattern = re.compile(r'((?<!\/)\b\w+\:\s*\"?[\-\w\.]*\"?),?')
MonsterList = defaultdict(dict)

for match in re.finditer(monsterExtractionPattern, monsters):
    monster = match.group(0)
    monsterName = monster.split(':')[0]

    for attr in re.finditer(attributePattern, monster.split('{')[1]):
        attribute = attr.group(0)
        [key, value] = attribute.split(':')
        MonsterList[key][monsterName] = value.strip('\",')

MON = pd.DataFrame(MonsterList)

# =============================================================================
# # To excel
# =============================================================================

excel = ExcelWriter("MonsterList.xlsx", engine='xlsxwriter')
MON.to_excel(excel, 'Material data')
excel.save()
