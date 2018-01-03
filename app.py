
import wx
import threading
import gui

import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

from stock import Stock
import numpy as np
import pandas as pd

# global dictionary for parameter choosing
MARKET = {
    "SH and SZ": "hs&sz.txt",
    "HK": "hk.txt"
}

RULE = {
    "MA Cross(10, 20)": "MA_cross",
    "Doji": "Doji"
}


class App(gui.MainFrame):
    #constructor
    def __init__(self, parent):
        #initialize parent class
        gui.MainFrame.__init__(self, parent)
        
        # dataviewlist column name
        self.stockListCtrl.AppendTextColumn("StockCode")

        # use panel as output for matplotlib to plot chart
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.right_panel, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.right_panel.SetSizer(self.sizer)
        self.right_panel.Fit()

        # dict for the stocks seleted
        self.stock_dict = {}

    # function to draw the chart of a stock given the freqency
    def draw(self, code, freq):
        self.axes.clear()
        s = self.stock_dict[code]
        s.wxPlot(freq, self.axes)
        self.right_panel.Layout()
        
    # function doing the stock selection
    def ForSelection(self):
        # clear the previous output
        self.stockListCtrl.DeleteAllItems()
        self.stock_dict = {}

        # get the parameters needed
        market = MARKET[self.market_radioBox.GetStringSelection()]
        rule = RULE[self.rule_radioBox.GetStringSelection()]
        freq = self.frequency_radioBox.GetStringSelection()
        code_list = pd.read_csv(market, dtype = 'str').code.tolist()
        
        # conduct the stock selection
        update_list = []
        length = len(code_list)
        for i, code in enumerate(code_list):
            # print(code)
            if market == "hs&sz.txt":
                s = Stock(code)
            else:
                s = Stock(code, market = "HK")
            function = s.__getattribute__(rule)
            if not s.is_suspended and function(freq):
                self.stock_dict[code] = s
                update_list.append([code])
            
            # this will update the process bar
            self.select_gauge.SetValue((i+1)*100//length) 
            wx.Yield()

        # show the output to the dataviewlist 
        for i in update_list:
            self.stockListCtrl.AppendItem(i)

    # conduct the stock selection in the async way
    def MakeSelection( self, event ):
        threading.Thread(target=self.ForSelection).start()
        
    # changing the draw freqency will upate the chart
    def ReDrawFreqency( self, event ):
        row = self.stockListCtrl.SelectedRow
        code = self.stockListCtrl.GetTextValue(row, 0)
        freq = self.frequency_radioBox_draw.GetStringSelection()
        self.draw(code, freq)
    
    # changing the selected stock code will udpate the chart 
    def ReDrawPicture( self, event ):
        row = self.stockListCtrl.SelectedRow
        code = self.stockListCtrl.GetTextValue(row, 0)
        freq = self.frequency_radioBox_draw.GetStringSelection()
        self.draw(code, freq)



if __name__ == "__main__":
    app = wx.App(False)
    frame = App(None)
    frame.Show(True)
    app.MainLoop()
