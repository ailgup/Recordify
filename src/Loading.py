import wx
import wx.xrc
import wx.adv

###########################################################################
# Class Loading
###########################################################################


class Loading (wx.Dialog):

    def __init__(self, parent):
        self.loaded = False
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                           pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(),
                             70, 90, 90, False, "Arial"))
        self.SetBackgroundColour(wx.Colour(50, 50, 50))

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(
            self, wx.ID_ANY, u"Loading...", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetFont(
            wx.Font(16, 70, 90, 90, False, "Gotham Medium"))
        self.m_staticText5.SetForegroundColour(wx.Colour(255, 255, 255))

        bSizer2.Add(self.m_staticText5, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL, 5)
        ani = wx.adv.Animation()
        ani.LoadFile(u"loading.gif")
        self.m_animCtrl2 = wx.adv.AnimationCtrl(
            self, wx.ID_ANY,  ani, wx.DefaultPosition, wx.DefaultSize)

        self.m_animCtrl2.Play()
        bSizer2.Add(self.m_animCtrl2, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer2)
        self.Layout()
        bSizer2.Fit(self)

        self.Centre(wx.BOTH)
        self.loaded = True
        self.Show()
        print("Show me")

    def __del__(self):
        pass
