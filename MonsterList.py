# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 09:20:45 2021

@author: lovro selic
@version 0.2.2

private tool for creation of excel files from monster
definition in MAP module of CrawlMaster game
"""

import regex as re
import pandas as pd
from pandas import ExcelWriter
from collections import defaultdict

# _file = "Monsters.js"
_file = "C:/Users/lovro/OneDrive/Documents/JS/CrawlMaster/MAP_CrawlMaster.js"
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
MON.drop(["behaviourArguments"], inplace=True, axis=1)

# =============================================================================
# # Calculated attributes
# =============================================================================

MON['attack'] = pd.to_numeric(MON['attack'])
MON['defense'] = pd.to_numeric(MON['defense'])
MON['magic'] = pd.to_numeric(MON['magic'])
MON['health'] = pd.to_numeric(MON['health'])
MON['xp'] = pd.to_numeric(MON['xp'])

MON['ADN'] = MON['attack'] + MON['defense'] + MON['magic']
MON['F'] = MON['xp'] / MON['ADN']
MON['Xf'] = MON['xp'] / (MON['ADN'] + MON['health'])

# =============================================================================
# # To excel
# =============================================================================

excel = ExcelWriter("MonsterList.xlsx", engine='xlsxwriter')
MON.to_excel(excel, 'Material data')
excel.save()
