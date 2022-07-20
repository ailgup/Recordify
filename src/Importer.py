# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Importer
###########################################################################

class Importer ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Importing Songs", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Importing Songs", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        self.m_staticText10.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer2.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )
        
        gSizer2 = wx.GridSizer( 1, 3, 0, 0 )
        
        self.current_song = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.current_song.Wrap( -1 )
        gSizer2.Add( self.current_song, 0, wx.ALIGN_RIGHT|wx.ALL, 10 )
        
        self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 0 ) 
        gSizer2.Add( self.m_gauge1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )
        
        self.total_songs = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.total_songs.Wrap( -1 )
        gSizer2.Add( self.total_songs, 0, wx.ALL, 10 )
        
        
        bSizer2.Add( gSizer2, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.current_name = wx.StaticText( self, wx.ID_ANY, u"Waiting...", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.current_name.Wrap( -1 )
        bSizer2.Add( self.current_name, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Stop Import", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        bSizer2.Fit( self )
        
        self.Centre( wx.BOTH )
        self.m_button1.Bind( wx.EVT_BUTTON, self.kill )
	
    ## Added post
    def kill(self, event):
        self.Destroy()
    def dataThread(self,url):
        print("Spawn Thread")

        for line in url.split('\n'):
            if("https://open.spotify.com/track/" in url):
                tmp = b.getTrackInfo(
                    (line.lstrip("https://open.spotify.com/track/")).rstrip('\n'))
                self.frame.addItemtoQ(tmp)
            else:
                wx.MessageBox(
                    "This is not a Spotify Song\n\nTo use properly drag a song, or many songs, over from the Spotify application", "Error", wx.OK | wx.ICON_ERROR)
        self.window.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        return
    
    def __del__( self ):
        pass
    

