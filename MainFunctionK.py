
import json
import pandas as pd

import IndexCalK
import TradeRulesK
import numpy as np



# buy index: Ma1XMa2Buy,angle,kCount,underK60,k60GoUp,kUp,amountUp,RSIBuy
# sell index: Ma1XMa2Sell,pressureDown,amountDown,LJBL,RSISell

rule_data=np.array(pd.read_csv('ruleSetK.csv'))

dataList = ["BTC_1min_20200614","BTC_1min_20200616",
            "BTC_1min_20200620","BTC_1min_20200621","BTC_1min_20200623"]
for data in dataList:
    ruleObj ={}
    for rule in rule_data:
        ruleObj[rule[0]]=TradeRulesK.rules(rule[1:])


    with open(data+".json", 'r') as load_f:
        kline_1min = json.load(load_f)

    safeAccount = [i for i in range(len(ruleObj))]


    for i in range(500,len(kline_1min) - 120):
        kline = (pd.DataFrame.from_dict(kline_1min[i:i + 120]))[['id', 'close', 'high', 'low', 'open', 'amount']]
        closed = kline['close'].values
        opened = kline['open'].values
        highed = kline['high'].values
        lowed = kline['low'].values
        amounted = kline['amount'].values
        [maDown_list,maUp_list,k60GoDown,kDown,
         amountDown,preKamountDown,amountUp,preKamountUp,
         macdBuy,longLow,rsi_forward,rsi]=IndexCalK.indexCal(closed,opened,highed,lowed,amounted)

        processAccount = safeAccount.copy()
        for j in processAccount:
            ruleObj[j].updateAccount(closed[-1],highed[-1])
            if ruleObj[j].account_alive==False:
                safeAccount.remove(j)
                continue
            if kDown*ruleObj[j].kDown==0 and k60GoDown*ruleObj[j].k60GoDown==0:
                for maDown in maDown_list:
                    if (maDown[0]== ruleObj[j].MaBuy and maDown[1]>=ruleObj[j].angle and maDown[2]>=ruleObj[j].kCount and
                            max(amountDown,preKamountDown*ruleObj[j].preKamountDown)>=ruleObj[j].amountDown):
                        ruleObj[j].buyOperation(closed[-1])
                        break

            if closed[-1]>ruleObj[j].costPrice*(1.01) or closed[-1]<ruleObj[j].costPrice*(1-ruleObj[j].winRate):
                ruleObj[j].sellPosition=1
                ruleObj[j].sellOperation(closed[-1])


            if ruleObj[j].MaSell in maUp_list and max(amountUp,preKamountUp)>ruleObj[j].amountUp:
                ruleObj[j].sellPosition = 1
                ruleObj[j].sellOperation(closed[-1])

            if ruleObj[j].macd==1 and macdBuy==1:
                ruleObj[j].sellPosition = 1
                ruleObj[j].sellOperation(closed[-1])

            if ruleObj[j].longLow==1 and longLow==1:
                ruleObj[j].sellPosition = 0.5
                ruleObj[j].sellOperation(closed[-1])

            if rsi_forward<ruleObj[j].RSI and rsi_forward<rsi:
                ruleObj[j].sellPosition = 0.5
                ruleObj[j].sellOperation(closed[-1])



        print(i)


    result = []

    for i in safeAccount:
        [account_money, trade_count] = ruleObj[i].outPut()
        if account_money>=900:
            result.append([account_money,trade_count,i])

    result.sort(reverse=True)
    print(result[0])
    a = pd.DataFrame(result)
    a.to_csv(data+'_RulesResultK.csv')
