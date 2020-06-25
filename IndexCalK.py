

import talib



def indexCal(closed,opened,highed,lowed,amounted):

    ma5 = talib.SMA(closed, timeperiod=5)
    ma20 = talib.SMA(closed, timeperiod=20)
    ma30 = talib.SMA(closed, timeperiod=30)
    ma60 = talib.SMA(closed, timeperiod=60)
    rsi = talib.RSI(closed, timeperiod=14)
    macd, signal, hist = talib.MACD(closed, fastperiod=12, slowperiod=26, signalperiod=9)

    maCal_list=[[ma5,ma20,100],[ma5,ma30,150],[ma5,ma60,300]]

    maDown_list =[]
    maUp_list = [0]
    for [m1,m2,n] in maCal_list:
        if n!=100 and m1[-1] < m2[-1] and m1[-2] > m2[-2]:
            angle = ((m1[-2]-m1[-1])/m1[-2]+(m1[-3]-m1[-2])/m1[-3])*10000
            for i in range(3, 30):
                if (m1[-i] < m2[-i]):
                    break
                else:
                    kCount += 1
            maDown_list.append([n,angle,kCount])

        if m1[-1] > m2[-1] and m1[-2] < m2[-2]:
            maUp_list.append(n)



    #0 is satisfied ,1 is not

    k60GoDown = 0
    a = [ma60[-3], ma60[-4], ma60[-5]]
    if a != sorted(a):
        k60GoDown = 1

    kDown = 0
    if closed[-1]>opened[-1]:kDown = 1


    amountDown = 0
    preKamountDown = 0
    amountUp = 0
    preKamountUp = 0
    if kDown==0: amountDown = amounted[-1]/amounted[-2]
    else: amountUp = amounted[-1]/amounted[-2]

    if closed[-2]<opened[-2]:preKamountDown =amounted[-2]/amounted[-3]
    else:preKamountUp = amounted[-2]/amounted[-3]

    # 1 is satisfied ,0 is not
    macdBuy = 0
    if hist[-1] > 0 and macd[-1] > signal[-1] and macd[-2] < signal[-2] and amounted[-1] / max(1, amounted[-2]) > 2:
        for i in range(1, 6):
            if rsi[-i] < 30:
                macdBuy = 1
                break

    longLow = 0
    if highed[-2] - lowed[-2]!=0:
        lowPointLong = min(closed[-2], opened[-2]) - lowed[-2]
        highPointLong = highed[-2] - max(closed[-2], opened[-2])
        lowPointLongRate = lowPointLong / (highed[-2] - lowed[-2])
        highPointLongRate = highPointLong / (highed[-2] - lowed[-2])
        if lowPointLong > 20 and lowPointLongRate > 0.7 and highPointLongRate < 0.1 and rsi[-2] < 30 and closed[-1]>opened[-1]:
            longLow = 1





    return [maDown_list,maUp_list,k60GoDown,kDown,amountDown,preKamountDown,amountUp,preKamountUp,macdBuy,longLow,rsi[-2],rsi[-1]]









