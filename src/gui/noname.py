# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Jun 17 2015)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
# Class MyFrame1
###########################################################################


class MyFrame1 (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Recordify", pos=wx.DefaultPosition, size=wx.Size(
            514, 387), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))

        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Settings", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.AppendItem(self.m_menuItem1)

        self.m_menuItem2 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.AppendItem(self.m_menuItem2)

        self.m_menu1.AppendSeparator()

        self.m_menuItem3 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.AppendItem(self.m_menuItem3)

        self.m_menubar1.Append(self.m_menu1, u"File")

        self.SetMenuBar(self.m_menubar1)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        gSizer5 = wx.GridSizer(0, 2, 0, 0)

        fgSizer1 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.HORIZONTAL)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.m_bpButton1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(
            u"../play.bmp", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW | wx.NO_BORDER)

        self.m_bpButton1.SetBitmapHover(wx.NullBitmap)
        fgSizer1.Add(self.m_bpButton1, 0, wx.ALL, 5)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(
            u"../temp_album.jpg", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.Size(50, 50), 0)
        fgSizer1.Add(self.m_bitmap1, 1, wx.ALL, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.currentSong = wx.StaticText(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentSong.Wrap(-1)
        bSizer2.Add(self.currentSong, 0, wx.ALL, 3)

        self.currentArtist = wx.StaticText(
            self, wx.ID_ANY, u"Not Recording", wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentArtist.Wrap(-1)
        bSizer2.Add(self.currentArtist, 1, wx.ALL | wx.EXPAND, 3)

        self.currentAlbum = wx.StaticText(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentAlbum.Wrap(-1)
        bSizer2.Add(self.currentAlbum, 0, wx.ALL, 3)

        fgSizer1.Add(bSizer2, 0, 0, 5)

        gSizer5.Add(fgSizer1, 0, 0, 5)

        self.m_bpButton2 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(
            u"../folder.bmp", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW | wx.NO_BORDER)
        gSizer5.Add(self.m_bpButton2, 0, wx.ALL |
                    wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer5.Add(gSizer5, 1, wx.EXPAND, 5)

        fgSizer2 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer2.AddGrowableCol(1)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.left_status = wx.StaticText(
            self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.left_status.Wrap(-1)
        fgSizer2.Add(self.left_status, 0, wx.ALL, 5)

        bSizer51 = wx.BoxSizer(wx.VERTICAL)

        self.m_gauge1 = wx.Gauge(
            self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(-1, -1), wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(0)
        bSizer51.Add(self.m_gauge1, 0, wx.ALL |
                     wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        fgSizer2.Add(bSizer51, 1, wx.EXPAND, 5)

        self.right_status = wx.StaticText(
            self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.right_status.Wrap(-1)
        fgSizer2.Add(self.right_status, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer5.Add(fgSizer2, 0, wx.EXPAND, 5)

        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        self.m_listCtrl1 = wx.ListCtrl(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON)
        self.m_listCtrl1.SetForegroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.m_listCtrl1.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.m_listCtrl1.SetToolTipString(
            u"Drag songs here from the Spotify application")

        bSizer1.Add(self.m_listCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        gSizer3 = wx.GridSizer(1, 2, 0, 0)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, u"Remove Selected Song(s)", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.m_button1, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button2 = wx.Button(
            self, wx.ID_ANY, u"Remove All Songs", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.m_button2, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(gSizer3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
