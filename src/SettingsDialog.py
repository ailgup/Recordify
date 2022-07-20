import wx
import wx.xrc

#Custom widget with the heat bar graph
class Widget(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, size=(330, 30), style=wx.SUNKEN_BORDER)
        
        self.parent = parent
        self.font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.cw=0

    def OnPaint(self, event):
    
        num = range(10, 110, 10)
        dc = wx.PaintDC(self)
        dc.SetFont(self.font)
        w, h = self.GetSize()


        step = int(round(w / 10.0))

        j = 0

        till = (w / 100.0) * self.cw
        full = (w / 100.0) * 90

        dc.SetPen(wx.Pen('#FF9999'))
        dc.SetBrush(wx.Brush('#FF9999'))
        dc.DrawRectangle(0, 0, w, 30)
        
        dc.SetPen(wx.Pen('#98FB98'))
        dc.SetBrush(wx.Brush('#98FB98'))
        dc.DrawRectangle(93, 0, 30, 30)
        
        if self.cw < 40 and self.cw > 30:
            text="Spotify volume is good to go!"
            loc=150 
        else:
            text="Set Spotify volume, so it is in green zone" 
            loc=120
        dc.SetPen(wx.Pen("#000000"))
        dc.SetBrush(wx.Brush("#000000"))
        dc.DrawRectangle(self.cw*3.1, 0, 2, 30)
        dc.DrawCircle(self.cw*3.1,15,3)    
        
        dc.SetPen(wx.Pen('#5C5142'))
        dc.DrawText(text,loc,5)

    def OnSize(self, event):
        self.Refresh()

class SettingsDialog (wx.Dialog):
    open=False
    def volumeLoop(self):
        while open:
             try:
                 vol=int(self.backend.getVolume()*100)
                 vol_str=str(vol)+'%'
                 self.m_staticText6.SetLabel(vol_str)
                 self.w.cw=vol
                 self.w.Refresh()
             except RuntimeError:
                return
    def __init__(self, parent, backend, audio, curr_audio, btrt, file, isPaused):
        
        self.backend=backend
        self.open=True
        self.audio = audio
        self.bitrate_options = btrt
        self.file = file
        
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings",
                           pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        
        self.w=Widget(self,wx.ID_ANY)
        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        gSizer1 = wx.GridBagSizer(15,15)

        self.m_staticText1 = wx.StaticText(
            self, wx.ID_ANY, u"Audio Output", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        gSizer1.Add(self.m_staticText1, wx.GBPosition(0,0),wx.GBSpan(1,1), wx.ALL | wx.ALIGN_RIGHT)

        m_choice1Choices = self.audio
        self.m_choice1 = wx.Choice(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(curr_audio)
        gSizer1.Add(self.m_choice1, wx.GBPosition(0,1),wx.GBSpan(1,1), wx.ALL)

        self.m_staticText2 = wx.StaticText(
            self, wx.ID_ANY, u"Import Song List", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gSizer1.Add(self.m_staticText2, wx.GBPosition(1,0),wx.GBSpan(1,1), wx.ALL | wx.ALIGN_RIGHT)

        self.m_filePicker1 = wx.FilePickerCtrl(
            self, wx.ID_ANY, self.file, u"Select a file", u"*.txt", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        gSizer1.Add(self.m_filePicker1, wx.GBPosition(1,1),wx.GBSpan(1,1), wx.ALL)

        self.m_staticText3 = wx.StaticText(
            self, wx.ID_ANY, u"Output Bitrate", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gSizer1.Add(self.m_staticText3, wx.GBPosition(2,0),wx.GBSpan(1,1), wx.ALL |
                    wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        bitrateChoices = [u"128", u"160", u"320"]
        self.bitrate = wx.Choice(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, bitrateChoices, 0)
        self.bitrate.SetSelection(bitrateChoices.index(self.bitrate_options))
        bSizer3.Add( self.bitrate, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )

        self.m_staticText4 = wx.StaticText(
            self, wx.ID_ANY, u"kbps", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        bSizer3.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )

        gSizer1.Add(bSizer3, wx.GBPosition(2,1),wx.GBSpan(1,1), wx.EXPAND)
        
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Volume", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        gSizer1.Add( self.m_staticText5, wx.GBPosition(3,0),wx.GBSpan(1,1), wx.ALL|wx.ALIGN_RIGHT )
        
        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Calculating", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        self.m_staticText6.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        gSizer1.Add( self.m_staticText6, wx.GBPosition(3,1),wx.GBSpan(1,1), wx.ALL )
        
        #self.slider=wx.Slider(self, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize , wx.SL_VALUE_LABEL)
        #self.slider.SetTick(30)
        #self.slider.SetTick(40)
        gSizer1.Add( self.w, wx.GBPosition(4,0),wx.GBSpan(1,2), wx.ALL | wx.EXPAND )

        self.save = wx.Button(self, wx.ID_ANY, u"Save",
                              wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.save, wx.GBPosition(5,0),wx.GBSpan(1,1), wx.ALL | wx.ALIGN_RIGHT)

        self.cancel = wx.Button(
            self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.cancel, wx.GBPosition(5,1),wx.GBSpan(1,1), wx.ALL)
        self.cancel.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())

        self.SetSizer(gSizer1)
        self.Layout()
        gSizer1.Fit(self)

        self.Centre(wx.BOTH)
        if (not isPaused):
            self.Disable()
        self.Bind(wx.EVT_CLOSE, self.on_Close)



    def on_Close(self, event):
        self.open=False
        self.Destroy()
    def Disable(self):
        self.bitrate.Enable(False)
        self.m_choice1.Enable(False)
        self.m_filePicker1.Enable(False)
        self.save.Enable(False)
