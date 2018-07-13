
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


# In[2]:

# 考虑本金年单利、年复利、期复利的整存算法
def DepositCumulation(Y5,Y3,Y2,Y1,Money,HowManyYears):
    #
    Deposit = pd.DataFrame()
    Deposit['rate'] = [Y5,Y3,Y2,Y1]
    Deposit['rate_check'] = [0,0,0,0]
    # 各存期存款年限计算
    Deposit['years'] = [5*(HowManyYears//5),
                        3*((HowManyYears-5*(HowManyYears//5))//3),
                        2*((HowManyYears-5*(HowManyYears//5)-3*((HowManyYears-5*(HowManyYears//5))//3))//2),
                        (HowManyYears-5*(HowManyYears//5)-3*((HowManyYears-5*(HowManyYears//5))//3)-2*((HowManyYears-5*(HowManyYears//5)-3*((HowManyYears-5*(HowManyYears//5))//3))//2))]
    Deposit.loc[Deposit['years']>0,'rate_check'] = 1 
    # 总利率计算（年单利）
    rate_A = 1+Y5/100*Deposit['years'][0]+Y3/100*Deposit['years'][1]+Y2/100*Deposit['years'][2]+Y1/100*Deposit['years'][3]
    # 总利率计算（年复利）
    rate_B = ((1+Y5/100)**Deposit['years'][0])*((1++Y3/100)**Deposit['years'][1])*((1++Y2/100)**Deposit['years'][3])*((1++Y3/100)**Deposit['years'][3])
    # 总利率计算（期复利）
    rate_C = (((1+Y5/100*5*Deposit['rate_check'][0])**(Deposit['years'][0]/5))
              *((1+Y3/100*3*Deposit['rate_check'][1])**(Deposit['years'][1]/3))
              *((1+Y2/100*2*Deposit['rate_check'][2])**(Deposit['years'][2]/2))
              *((1+Y1/100*1*Deposit['rate_check'][3])**(Deposit['years'][3]/1)))
    # 总利息计算
    rates = rate_C
    interest = Money*(rates-1)
    # 本金和利息总和计算
    principal_with_interest = Money*rates
    # 平均年利息
    interest_average = Money*(rates-1)/HowManyYears
    # 
    Cumulation = pd.DataFrame([[Money,HowManyYears,rate_A,rate_B,rate_C,interest,principal_with_interest,interest_average]], columns=[u'存款金额(元)',u'存款年限(年)',u'总年单利(%)',u'总年复利(%)',u'总期复利(%)',u'利息(元)',u'本息(元)',u'平均年利息'])
    
    return Cumulation.round(3)


# In[3]:

# 考虑本金年单利、年复利、期复利的每年累积整存整存算法
def DepositCumulationMoneyEveryYears(Y5,Y3,Y2,Y1,Money,HowManyYears):
    # 每年固定存入金额
    MoneyEveryYears = Money
    # 累积存款年限(Accumulated Deposit Years)
    ADY = HowManyYears
    Accumulated_Deposit = pd.DataFrame(np.arange(1,ADY+1),columns=[u'存入次数'])
    for i in range(0,ADY):
        Yr5 = 5*((ADY-i)//5)
        Yr3 = 3*(((ADY-i)-5*((ADY-i)//5))//3)
        Yr2 = 2*(((ADY-i)-5*((ADY-i)//5)-3*(((ADY-i)-5*((ADY-i)//5))//3))//2)
        Yr1 = ((ADY-i)-5*((ADY-i)//5)-3*(((ADY-i)-5*((ADY-i)//5))//3)-2*(((ADY-i)-5*((ADY-i)//5)-3*(((ADY-i)-5*((ADY-i)//5))//3))//2))
        Yc5 = 0
        Yc3 = 0
        Yc2 = 0
        Yc1 = 0
        if Yr5 > 0:
            Yc5 = 1
        if Yr3 > 0:
            Yc3 = 1
        if Yr2 > 0:
            Yc2 = 1
        if Yr1 > 0:
            Yc1 = 1
        rate_i = ((1+Y5/100*5*Yc5)**(Yr5/5)
                  *(1+Y3/100*3*Yc3)**(Yr3/3)
                  *(1+Y2/100*2*Yc2)**(Yr2/2)
                  *(1+Y1/100*1*Yc1)**(Yr1/1))
        Accumulated_Deposit.loc[i:i,u'存入年限(年)'] = ADY-i
        Accumulated_Deposit.loc[i:i,u'累积存入本金(元)'] = MoneyEveryYears*(i+1)
        Accumulated_Deposit.loc[i:i,u'每笔利率(%)'] = rate_i
        Accumulated_Deposit.loc[i:i,u'每笔利息(元)'] = MoneyEveryYears*(rate_i-1)
        Accumulated_Deposit.loc[i:i,u'每笔本息(元)'] = MoneyEveryYears*rate_i
    # 合计
    Accumulated_Deposit.loc[u'合计'] = Accumulated_Deposit.apply(lambda x: x.sum())
    Accumulated_Deposit.loc[u'合计',0:4] = ''
    
    return Accumulated_Deposit.round(3)


# In[4]:

# 考虑本金年单利、年复利、期复利的再次整存算法
def DepositCumulationMoneyAgainYears(Y5,Y3,Y2,Y1,Money,MoneyAgainYears,HowManyYears,AgainYears):
    #
    Deposit = pd.DataFrame()
    Deposit['rate'] = [Y5,Y3,Y2,Y1]
    Deposit['rate_check'] = [0,0,0,0]
    # 各存期存款年限计算
    Deposit['years'] = [5*(AgainYears//5),
                        3*((AgainYears-5*(AgainYears//5))//3),
                        2*((AgainYears-5*(AgainYears//5)-3*((AgainYears-5*(AgainYears//5))//3))//2),
                        (AgainYears-5*(AgainYears//5)-3*((AgainYears-5*(AgainYears//5))//3)-2*((AgainYears-5*(AgainYears//5)-3*((AgainYears-5*(AgainYears//5))//3))//2))]
    Deposit.loc[Deposit['years']>0,'rate_check'] = 1 
    # 总利率计算（年单利）
    rate_A = 1+Y5/100*Deposit['years'][0]+Y3/100*Deposit['years'][1]+Y2/100*Deposit['years'][2]+Y1/100*Deposit['years'][3]
    # 总利率计算（年复利）
    rate_B = ((1+Y5/100)**Deposit['years'][0])*((1++Y3/100)**Deposit['years'][1])*((1++Y2/100)**Deposit['years'][3])*((1++Y3/100)**Deposit['years'][3])
    # 总利率计算（期复利）
    rate_C = (((1+Y5/100*5*Deposit['rate_check'][0])**(Deposit['years'][0]/5))
              *((1+Y3/100*3*Deposit['rate_check'][1])**(Deposit['years'][1]/3))
              *((1+Y2/100*2*Deposit['rate_check'][2])**(Deposit['years'][2]/2))
              *((1+Y1/100*1*Deposit['rate_check'][3])**(Deposit['years'][3]/1)))
    # 总利息计算
    rates = rate_C
    interest = MoneyAgainYears*(rates-1)
    # 本金和利息总和计算
    principal_with_interest = MoneyAgainYears*rates
    # M年总利息
    interest_all = MoneyAgainYears*rates-Money*HowManyYears
    # 平均年利息
    interest_average = (MoneyAgainYears*rates-Money*HowManyYears)/(HowManyYears+AgainYears)
    # 
    Cumulation = pd.DataFrame([[MoneyAgainYears,AgainYears,rate_A,rate_B,rate_C,interest,principal_with_interest,interest_all,interest_average]], columns=[u'存款金额(元)',u'存款年限(年)',u'总年单利(%)',u'总年复利(%)',u'总期复利(%)',u'利息(元)',u'本息(元)',u'总利息',u'平均年利息'])
    
    return Cumulation.round(3)

