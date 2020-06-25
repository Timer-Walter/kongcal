

class rules:


    def __init__(self,rule):
        self.MaBuy = rule[0]
        self.angle = rule[1]
        self.kCount = rule[2]
        self.k60GoDown = rule[3]
        self.kDown = rule[4]
        self.preKamountDown = rule[5]
        self.amountDown = rule[6]
        self.MaSell = rule[7]
        self.amountUp = rule[8]
        self.macd= rule[9]
        self.longLow= rule[10]
        self.RSI= rule[11]
        self.winRate = rule[12]



        self.rate = 10
        self.margin_available = 1000
        self.margin_frozen = 0
        self.volume = 0
        self.price = 0
        self.costPrice = 0
        self.tradeCount = 0
        self.account_alive = True
        self.buyPosition = 0.6
        self.sellPosition = 1



    def updateAccount(self,closedPrice,highPrice):
        if (self.margin_available + self.margin_frozen + (self.price-highPrice) * self.volume) <= 800:
            self.account_alive = False
        # 更新账户金额
        self.margin_available += (self.price - closedPrice) * self.volume
        self.price = closedPrice


    def buyOperation(self,closedPrice):
        buyPrice = closedPrice * (1-0.001)
        if self.margin_available > 0 and self.buyPosition > 0:
            margin_available_use = self.margin_available * self.buyPosition * self.rate * (1 - 0.0003)
            volume_add = margin_available_use / buyPrice
            self.volume += volume_add
            self.margin_frozen += self.margin_available * self.buyPosition
            self.margin_available -= self.margin_available * self.buyPosition
            self.tradeCount +=1
            self.costPrice = closedPrice

    def sellOperation(self,closedPrice):
        if self.volume > 0 and self.sellPosition > 0:
            self.margin_available += self.margin_frozen * self.sellPosition
            self.margin_frozen -= self.margin_frozen * self.sellPosition
            self.margin_available -= self.volume * self.sellPosition * closedPrice * 0.001
            self.volume -= self.volume * self.sellPosition
            self.tradeCount +=1
            self.costPrice = 0


    def outPut(self):
        account_money = 0
        trade_count = 0
        if self.account_alive==True:
            account_money = self.margin_available + self.margin_frozen
            trade_count = self.tradeCount
        return [account_money,trade_count]




