# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 22:36:51 2021

@author: Drps1
"""

import pandas as pd
import numpy as np
import math
import datetime

# Интерполятор из прошлого задания, воспринимающий даты.
def IntpExp(ondate, marketdata):    
    if ondate < min(marketdata['date']):
        print('interpolated date is < today')
    elif ondate <= max(marketdata['date']):
        i = 0
        while marketdata['date'][i] < ondate:
            i = i + 1
        lentox = (ondate - marketdata.iloc[i][0]).days
        xlen = (marketdata.iloc[i][0] - marketdata.iloc[i-1][0]).days
        ylen = marketdata.iloc[i][1] - marketdata.iloc[i-1][1]
        y = marketdata.iloc[i][1] + ylen * lentox / xlen
    elif ondate > max(marketdata['date']):
        lentox = (ondate - marketdata.iloc[-1][0]).days
        xlen = (marketdata.iloc[-1][0] - marketdata.iloc[-2][0]).days
        ylen = marketdata.iloc[-1][1] - marketdata.iloc[-2][1]
        y = marketdata.iloc[-1][1] + ylen * lentox / xlen
    return y
    
def IntpExp_array(ondates, marketdata):
    jlist = []
    for i in ondates:
        o = IntpExp(i, marketdata)
        jlist.append(o)
    return jlist

# Dummy функция по нахождению дисконт фактора для USD

def DFForeign( dates: datetime, asofdate: datetime):
    DFf = pd.DataFrame(columns=['date', 'df'])
    for i in range(len(dates)):
        k = math.exp( -0.02 * (dates[i] - asofdate).days/365) 
        DFf = DFf.append( pd.Series([dates[i], k], index = DFf.columns), ignore_index = True)
    return DFf

# Функция по выводу датафрейса с датами/дисконт факторами

def DFRub( Dates: datetime, MarketData, asofdate, spot):
    a = DFForeign( MarketData['date'], asofdate)
    b = MD['swap points']/10000 + spot
    c = pd.DataFrame(data = {'date': a['date'], 'DFrub': spot * a['df'] / b})
    
    t = pd.DataFrame(data = {'date': Dates, 'DFs': IntpExp_array(Dates, c)})
    return t

#_________________________________________
# дата оценки
asof = pd.to_datetime('08.11.2021')
Spot = 70

# Пример маркет даты
MD = pd.DataFrame( [
['09.11.2021', 172.624021264922],
['15.11.2021', 1209.2624879579],
['08.12.2021', 5197.28131373109],
['06.02.2022', 15707.8950166809],
['10.05.2022', 32309.7811383689],
['08.11.2022', 65921.9985936473],
['08.11.2023', 138052.154185267],
['07.11.2024', 216975.115513273]
], columns=['date', 'swap points'])
MD['date'] = pd.to_datetime(MD['date'], dayfirst = True)


#Пример дат, на которые надо найти рублевый DF'ы
RandomDates = pd.DataFrame( pd.to_datetime(['10.09.2022', '10.12.2022', '10.12.2029'], dayfirst = True))

#вызов функции
rubDFs = DFRub( RandomDates[0], MD, asof, Spot)

print(rubDFs)