# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 596,472 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		MainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter.Bind( wx.EVT_IDLE, self.m_splitterOnIdle )
		
		self.left_panel = wx.Panel( self.m_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		left_Sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter_h = wx.SplitterWindow( self.left_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter_h.Bind( wx.EVT_IDLE, self.m_splitter_hOnIdle )
		
		self.up_panel = wx.Panel( self.m_splitter_h, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		upSizer = wx.BoxSizer( wx.VERTICAL )
		
		upSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		market_radioBoxChoices = [ u"SH and SZ", u"HK" ]
		self.market_radioBox = wx.RadioBox( self.up_panel, wx.ID_ANY, u"Market", wx.DefaultPosition, wx.DefaultSize, market_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.market_radioBox.SetSelection( 0 )
		upSizer1.Add( self.market_radioBox, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		upSizer.Add( upSizer1, 1, wx.EXPAND, 5 )
		
		upSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		frequency_radioBoxChoices = [ u"d", u"30", u"5" ]
		self.frequency_radioBox = wx.RadioBox( self.up_panel, wx.ID_ANY, u"Frequency", wx.DefaultPosition, wx.DefaultSize, frequency_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.frequency_radioBox.SetSelection( 0 )
		upSizer2.Add( self.frequency_radioBox, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		upSizer.Add( upSizer2, 1, wx.EXPAND, 5 )
		
		upSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		rule_radioBoxChoices = [ u"MA Cross(10, 20)", u"Doji" ]
		self.rule_radioBox = wx.RadioBox( self.up_panel, wx.ID_ANY, u"Rule", wx.DefaultPosition, wx.DefaultSize, rule_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.rule_radioBox.SetSelection( 0 )
		upSizer3.Add( self.rule_radioBox, 0, wx.ALL, 5 )
		
		
		upSizer.Add( upSizer3, 1, wx.EXPAND, 5 )
		
		upSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.select_button = wx.Button( self.up_panel, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		upSizer4.Add( self.select_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.select_gauge = wx.Gauge( self.up_panel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.select_gauge.SetValue( 0 ) 
		upSizer4.Add( self.select_gauge, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		upSizer.Add( upSizer4, 1, wx.EXPAND, 5 )
		
		
		self.up_panel.SetSizer( upSizer )
		self.up_panel.Layout()
		upSizer.Fit( self.up_panel )
		self.down_panel = wx.Panel( self.m_splitter_h, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		downSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline1 = wx.StaticLine( self.down_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		downSizer.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		frequency_radioBox_drawChoices = [ u"d", u"30", u"5" ]
		self.frequency_radioBox_draw = wx.RadioBox( self.down_panel, wx.ID_ANY, u"Draw Frequency", wx.DefaultPosition, wx.DefaultSize, frequency_radioBox_drawChoices, 1, wx.RA_SPECIFY_ROWS )
		self.frequency_radioBox_draw.SetSelection( 0 )
		downSizer.Add( self.frequency_radioBox_draw, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stockListCtrl = wx.dataview.DataViewListCtrl( self.down_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		downSizer.Add( self.stockListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.down_panel.SetSizer( downSizer )
		self.down_panel.Layout()
		downSizer.Fit( self.down_panel )
		self.m_splitter_h.SplitHorizontally( self.up_panel, self.down_panel, 300 )
		left_Sizer.Add( self.m_splitter_h, 1, wx.EXPAND, 5 )
		
		
		self.left_panel.SetSizer( left_Sizer )
		self.left_panel.Layout()
		left_Sizer.Fit( self.left_panel )
		self.right_panel = wx.Panel( self.m_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_splitter.SplitVertically( self.left_panel, self.right_panel, 0 )
		MainSizer.Add( self.m_splitter, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( MainSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.select_button.Bind( wx.EVT_BUTTON, self.MakeSelection )
		self.frequency_radioBox_draw.Bind( wx.EVT_RADIOBOX, self.ReDrawFreqency )
		self.stockListCtrl.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.ReDrawPicture, id = wx.ID_ANY )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def MakeSelection( self, event ):
		event.Skip()
	
	def ReDrawFreqency( self, event ):
		event.Skip()
	
	def ReDrawPicture( self, event ):
		event.Skip()
	
	def m_splitterOnIdle( self, event ):
		self.m_splitter.SetSashPosition( 0 )
		self.m_splitter.Unbind( wx.EVT_IDLE )
	
	def m_splitter_hOnIdle( self, event ):
		self.m_splitter_h.SetSashPosition( 300 )
		self.m_splitter_h.Unbind( wx.EVT_IDLE )
	

