import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
import datetime 
from dateutil import relativedelta
import requests
import re
from io import StringIO
import numpy as np
import talib


# Stock class to handle the stock data
# so far it can handel data for 3 markets: Shanghai, Shenzhen, HongKong
# for 3 time frequency: day, 30 mins, 5 mins

# Shanghai and Shenzhen will get data easily via tushare
# HongKong is using google API(30mins, 5mins), for day prices, yahoo stop the old api, right now is using the webscraping
# it is slow and unstable, google API cannot provide day prices for long period

class Stock:

    stock_code = ''
    data_d = None
    data_30 = None
    data_5 = None

    is_suspended = None

    def __init__(self, stock_code, index = False, market = "ML"):

        if market not in ["ML", "HK"]:
            raise ValueError("market parameter should be ML or HK")

        self.stock_code = stock_code

        if market == "ML":
            #self.data_d =  ts.get_k_data(self.stock_code, index = index)
            self.data_d =  ts.get_k_data(self.stock_code, index = index, start = (datetime.date.today() + relativedelta.relativedelta(months=-12)).strftime("%Y-%m-%d"), end = datetime.date.today().strftime("%Y-%m-%d")).reset_index(drop = True)  
            self.data_30 = ts.get_k_data(self.stock_code, index = index, ktype = '30')
            self.data_5 =  ts.get_k_data(self.stock_code, index = index, ktype = '5')

        else:
            try:
                self.data_d =  self.__get_k_data_hk(self.stock_code, ktype = 'd')  
            except:
                pass
            self.data_30 = self.__get_k_data_hk(self.stock_code, ktype = '30')
            self.data_5 =  self.__get_k_data_hk(self.stock_code, ktype = '5')


        if self.data_d is None or len(self.data_d) == 0:
            latest_date = (datetime.datetime.today() + relativedelta.relativedelta(months=-12))
        else:
            latest_date = self.data_d.ix[len(self.data_d) - 1, 'date']
            latest_date = datetime.datetime.strptime(latest_date, "%Y-%m-%d")
            
        if (datetime.datetime.today() - latest_date) > datetime.timedelta(3, 64800, 0):
            self.is_suspended = 1
        else:
            self.is_suspended = 0

    # get HK data, use google api or yahoo webscraping
    def __get_k_data_hk(self, code, ktype):

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        if ktype == 'd':
            end_date = datetime.datetime.now()
            start_date = end_date + relativedelta.relativedelta(months=-24)

            r = requests.get('https://finance.yahoo.com/quote/{}.HK/history?p={}.HK'.format(code, code))
            p = re.compile(r'"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
            iter_result = p.finditer(r.text)
            crumb = next(iter_result).group(1)

            cookies = r.cookies
            url = "https://query1.finance.yahoo.com/v7/finance/download/{}.HK?period1={}&period2={}&interval=1d&events=history&crumb={}"
            r = requests.get(url.format(code, int(start_date.timestamp()), int(end_date.timestamp()), crumb), cookies = cookies)

            try: 
                data = pd.read_csv(StringIO(r.text))
            except:
                print(r.text)
            # data = raw.sort_values(by = ['Date']).reset_index(drop = True)

            if data.Close.dtype == np.dtype(object):
                final_result = data.loc[data["Close"]!="null", ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]
                final_result.reset_index(drop = True, inplace = True)
                final_result.rename(columns = {'Date': 'date', 'Open': 'open', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Volume': 'volume'}, inplace=True)
                final_result[['open', 'close', 'high', 'low', 'volume']] = final_result[['open', 'close', 'high', 'low', 'volume']].astype(float)
            else:
                final_result = data.loc[:, ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]
                final_result.rename(columns = {'Date': 'date', 'Open': 'open', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Volume': 'volume'}, inplace=True)
            return final_result

        else:

            if ktype == '5':
                interval = 60 * 5
                days = 10
            elif ktype == '30':
                interval = 60 * 30
                days = 20
            elif ktype == 'd':
                interval = 60 * 60 * 24
                days = 480
            else:
                print('Wrong ktype!')
                return
        
            result = []

            url_string = "http://finance.google.com/finance/getprices?q={0}".format(code)
            url_string += "&i={0}&x=HKG&p={1}d&f=d,o,h,l,c,v".format(interval, days)
            r = requests.get(url_string, headers=headers, stream=True)
            csv = list(r.iter_lines())
            for bar in range(7,len(csv)):
                if csv[bar].decode('UTF-8').count(',') != 5:
                    continue
                offset, close, high, low, open, volume = csv[bar].decode('UTF-8').replace('\n', '').split(',')
                if offset[0]=='a':
                    day = float(offset[1:])
                    offset = 0
                else:
                    offset = float(offset)
                open, high, low, close = [float(x) for x in [open, high, low, close]]
                dt = datetime.datetime.fromtimestamp(day + (interval * offset))
                result.append([dt, open, close, high, low, volume])

            final_result = pd.DataFrame(result, columns = ['date', 'open', 'close', 'high', 'low', 'volume'])
            return final_result

    
    # this function helps to get the open high low close prices in a proper format to plot
    def __get_ohlc(self, ktype):
        if ktype not in ['d', '30', '5']:
            raise ValueError("ktype parameter wrong!")

        if ktype == 'd':
            return list(zip(list(range(len(self.data_d.index))),
                    self.data_d.open, self.data_d.high, self.data_d.low, self.data_d.close))

        elif ktype == '30':
            return list(zip(list(range(len(self.data_30.index))),
                    self.data_30.open, self.data_30.high, self.data_30.low, self.data_30.close))

        elif ktype == '5':
            return list(zip(list(range(len(self.data_5.index))),
                    self.data_5.open, self.data_5.high, self.data_5.low, self.data_5.close))
        
        else:
            return None
        
    # normal plot using pyplot
    def plot(self, ktype):
        if ktype not in ['d', '30', '5']:
            print('Wrong input!')
            return None

        ohlc = self.__get_ohlc(ktype)

        fig = plt.figure(figsize=(18,7))
        ax = plt.subplot(1,1,1)
        c = candlestick_ohlc(ax, ohlc, width=0.6, colorup='r', colordown='g')
        plt.show()

    # plot to wxPython panel
    def wxPlot(self, ktype, ax):
        if ktype not in ['d', '30', '5']:
            print('Wrong input!')
            return None

        ohlc = self.__get_ohlc(ktype)
        c = candlestick_ohlc(ax, ohlc, width=0.6, colorup='r', colordown='g')
        



    ##############################################################
    # 2 simple rules to select stocks

    # MA crossing rule
    def MA_cross(self, ktype, ma1 = 10, ma2 = 20):
        if ktype not in ['d', '30', '5']:
            print('Wrong input!')
            return None
        data = np.array(self.__getattribute__("data_"+ktype)["close"])
        ma_1 = talib.MA(data, ma1)
        ma_2 = talib.MA(data, ma2)

        is_picked = ma_1[-1] > ma_2[-1] and ma_1[-2] < ma_2[-2]
        return is_picked


    # Doji pattern rule
    def Doji(self, ktype):
        if ktype not in ['d', '30', '5']:
            print('Wrong input!')
            return None
        data = self.__getattribute__("data_"+ktype)
        integer = talib.CDLDOJI(np.array(data["open"]), 
                            np.array(data["high"]), 
                            np.array(data["low"]), 
                            np.array(data["close"]))
        is_picked = integer[-2] == 100 and list(data["high"])[-2] < list(data["high"])[-3] and list(data["low"])[-2] < list(data["low"])[-3]
        
        return is_picked

