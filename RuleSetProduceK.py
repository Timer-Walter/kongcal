


import pandas as pd
import itertools


def produceRules():

    MaBuy_list= [150,300]
    angle_list = [0,2,3,4,5]
    kCount_list = [5,10,15,20]
    k60GoDown_list=[0,1]
    kDown_list=[0,1]
    preKamountDown_list = [0, 1]
    amountDown_list =[0,2,3,4,6,8]



    MaSell_list= [0,100,150,300]
    amountUp_list =[0,3,4,5,6]
    macd_list=[0,1]
    longLow_list=[0,1]
    RSI_list=[0,20,25,30]

    winRate = [0.02,0.03,0.04,0.05]



    rule_list = [MaBuy_list,angle_list,kCount_list,k60GoDown_list,kDown_list,
                 preKamountDown_list,amountDown_list,MaSell_list,
                 amountUp_list,macd_list,longLow_list,RSI_list,winRate]

    rule_data = []
    for x in itertools.product(*rule_list):
        rule_data.append(x)
    a = pd.DataFrame(rule_data)
    a.to_csv('ruleSetK.csv')

produceRules()