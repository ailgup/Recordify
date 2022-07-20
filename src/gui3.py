# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Jun 17 2015)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import datetime
import wx
import wx.xrc
import wx.adv
import threading
import time
import os
import ctypes
import sys
from wx.lib.pubsub import pub
import base64
import urllib.request
import urllib.parse
import webbrowser
from recorder import Backend
from SettingsDialog import SettingsDialog
from icons import Icons
from Importer import Importer
try:
    from BUILD_CONSTANTS import *
except ImportError:
    VERSION="0.0"
###########################################################################
# Class Recordify
###########################################################################
########################################################################


class MyURLDropTarget(wx.PyDropTarget):

    #----------------------------------------------------------------------
    def __init__(self, window):
        wx.DropTarget.__init__(self)
        self.window = window

        self.data = wx.URLDataObject()
        self.SetDataObject(self.data)

    def OnData(self, x, y, d):
        if not self.GetData():
            return wx.DragNone
        url = self.data.GetURL()
        open_dialog=url.count("\n")>1
        if open_dialog:
            self.imp = Importer(self.window)
            self.imp.Show()
        t=threading.Thread(target=self.dataThread,args=(url,open_dialog))
        t.start()
        return d
    def dataThread(self,url,open_dialog):
        time.sleep(.5)
        count=len(url.split("\n"))
        if open_dialog:
            self.imp.total_songs.SetLabel(str(count))
        i=1
        for line in url.split('\n'):
            if open_dialog:
                try:
                    if not self.imp.IsShown():
                        return
                except RuntimeError:
                    return
            if("https://open.spotify.com/track/" in url):
                tmp = b.getTrackInfo(
                    (line.lstrip("https://open.spotify.com/track/")).rstrip('\n'))
                add = True
                if(os.path.isfile(b.r.saveAs + "\\" + tmp.get("fileName") + ".mp3")):
                    result = wx.MessageBox('Found matching file\n' + tmp.get("fileName") + '.mp3\nDo you want to overwrite this?',
                                           'File Conflict', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    if(result is wx.NO):
                        add = False
                if(add):
                    try:
                        if open_dialog:
                            self.imp.current_song.SetLabel(str(i))
                            name=tmp.get("trackName","missing")
                            artist=tmp.get("artistName","missing")
                        
                            self.imp.current_name.SetLabel(str(name+" - "+artist))
                            self.imp.m_gauge1.SetValue(int(i/count*100))
                            self.imp.Layout()

                        frame.addItemtoQ(tmp)
                    except RuntimeError:
                        return
                i+=1
            else:
                wx.MessageBox(
                    "This is not a Spotify Song\n\nTo use properly drag a song, or many songs, over from the Spotify application", "Error", wx.OK | wx.ICON_ERROR)
        if open_dialog:
            self.imp.Destroy()
        return


from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class Recordify (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Recordify", pos=wx.DefaultPosition, size=wx.Size(
            514, 387), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(144, 144, 144))

        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Settings", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)

        self.m_menuItem2 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem2)

        self.m_menuItem5 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Remove Spotify Ads", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem5)

        self.m_menu1.AppendSeparator()

        self.m_menuItem3 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem3)

        self.m_menubar1.Append(self.m_menu1, u"File")

        self.SetMenuBar(self.m_menubar1)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        gSizer5 = wx.GridSizer(0, 2, 0, 0)

        self.fgSizer1 = wx.FlexGridSizer(0, 3, 0, 0)
        self.fgSizer1.SetFlexibleDirection(wx.HORIZONTAL)
        self.fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.m_bpButton1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(
            "play.bmp", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize)

        self.fgSizer1.Add(self.m_bpButton1, 0, wx.ALL, 5)

        self.m_bitmap1 = wx.StaticBitmap(
            self, wx.ID_ANY, wx.Bitmap(), wx.DefaultPosition, wx.DefaultSize, 0)
        self.fgSizer1.Add(self.m_bitmap1, 1, wx.ALL, 5)

        self.bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.currentSong = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentSong.Wrap(-1)
        self.bSizer2.Add( self.currentSong, 0, wx.ALL, 3 )

        self.currentArtist = wx.StaticText(
            self, wx.ID_ANY, u"Not Recording", wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentArtist.Wrap(-1)
        self.bSizer2.Add(self.currentArtist, 1, wx.ALL | wx.EXPAND, 3)

        self.currentAlbum = wx.StaticText(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentAlbum.Wrap(-1)
        self.bSizer2.Add(self.currentAlbum, 0, wx.ALL, 3)

        self.fgSizer1.Add(self.bSizer2, 0, 0, 5)

        gSizer5.Add(self.fgSizer1, 0, 0, 5)

        self.m_bpButton2 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(
            "folder.bmp", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize)
        gSizer5.Add(self.m_bpButton2, 0, wx.ALL |
                    wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer5.Add(gSizer5, 1, wx.EXPAND, 5)

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        fgSizer2 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer2.AddGrowableCol(1)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.left_status = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.left_status.Wrap(-1)
        fgSizer2.Add(self.left_status, 0, wx.ALL|wx.ALIGN_BOTTOM, 5)

        bSizer51 = wx.BoxSizer(wx.VERTICAL)

        self.m_gauge1 = wx.Gauge( self.m_panel2, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue(0)
        bSizer51.Add( self.m_gauge1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        

        fgSizer2.Add(bSizer51, 1, wx.EXPAND | wx.ALIGN_BOTTOM, 5)

        self.right_status = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.right_status.Wrap(-1)
        fgSizer2.Add(self.right_status, 0, wx.ALL | wx.ALIGN_RIGHT |wx.ALIGN_BOTTOM, 5)

        
        self.m_panel2.SetSizer( fgSizer2 )
        self.m_panel2.Layout()
        fgSizer2.Fit( self.m_panel2 )
        bSizer5.Add(self.m_panel2, 0, wx.ALL|wx.EXPAND, 5)

        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        self.m_listCtrl1 = wx.ListCtrl(
            self, -1, style=wx.LC_REPORT | wx.BORDER_NONE)  # | wx.SUNKEN_BORDER)

        self.m_listCtrl1.SetToolTip(
            u"Drag songs here from the Spotify application")
        col1 = wx.ListItem()
        col1.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        col1.Image = -1
        col1.Format = 0
        col1.Text = "Name"
        self.m_listCtrl1.InsertColumn(0, col1)
        self.m_listCtrl1.InsertColumn(1, 'Artist')
        self.m_listCtrl1.InsertColumn(2, 'Album')
        self.image_list = wx.ImageList(16, 16)

        self.imglistdict = {}

        self.imglistdict[0] = self.image_list.Add(
            wx.Bitmap(u"add.png", wx.BITMAP_TYPE_PNG))
        self.imglistdict[1] = self.image_list.Add(
            wx.Bitmap(u"speaker.png", wx.BITMAP_TYPE_PNG))
        self.imglistdict[2] = self.image_list.Add(
            wx.Bitmap(u"check.png", wx.BITMAP_TYPE_PNG))
        self.m_listCtrl1.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)
        bSizer1.Add(self.m_listCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        gSizer3 = wx.GridSizer(1, 3, 0, 0)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, u"Remove Selected Song(s)", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.m_button1, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button2 = wx.Button(
            self, wx.ID_ANY, u"Remove All Songs", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.m_button2, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        gSizer4 = wx.GridSizer(1, 2, 0, 0)

        self.m_button3 = wx.Button(
            self, wx.ID_ANY, u"▲", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3.SetMaxSize(wx.Size(25, -1))

        gSizer4.Add(self.m_button3, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button4 = wx.Button(
            self, wx.ID_ANY, u"▼", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button4.SetMaxSize(wx.Size(25, -1))

        gSizer4.Add(self.m_button4, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        gSizer3.Add(gSizer4, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer1.Add(gSizer3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        #####################
        # Stuff added by hand
        #####################
        self.m_panel2.Bind(wx.EVT_LEFT_DOWN,self.changeSlider)
        self.Bind(wx.EVT_MENU, self.startSettings, self.m_menuItem1)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, self.m_menuItem2)
        self.Bind(wx.EVT_MENU, self.removeAds, self.m_menuItem5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.deleteSelection)
        self.m_button2.Bind(wx.EVT_BUTTON, self.clearQueue)  # must write
        self.m_button3.Bind(wx.EVT_BUTTON, self.moveSelectionUp)
        self.m_button4.Bind(wx.EVT_BUTTON, self.moveSelectionDown)
        self.m_bpButton1.Bind(wx.EVT_BUTTON, self.playOrPause)
        self.m_bpButton2.Bind(wx.EVT_BUTTON, self.changeSaveAs)

        dt = MyURLDropTarget(self.m_listCtrl1)
        self.m_listCtrl1.SetDropTarget(dt)
        self.status = "play"
        self.slider = 'song'
        self.checkVersion()
# Connect Events

    def play(self):
        self.m_bpButton1.SetBitmapLabel(
            wx.Bitmap(b.r.cwd + "\\pause.bmp", wx.BITMAP_TYPE_ANY))
        self.status = 'pause'
        self.m_bpButton2.Enable(False)
        self.m_button2.Enable(False)
        self.m_menuItem1.Enable(False)
        if(len(b.song_queue) is 0):

            print("No songs in Q!")
            wx.MessageBox('There are no songs in the queue!\nDrag song(s) from the Spotify application to the Recordify.',
                          'Queue Empty', wx.OK | wx.ICON_INFORMATION)
            self.pause()
            return
            # self.updateQ()
        vol=b.getVolume()
        if(vol<0.3 or vol>0.4):
            if(wx.MessageBox('Spotify volume should be set at 30-40% for ideal recording.\nPress Yes to view volume percentage, No to ignore',
                          'Volume Warning',wx.YES_NO | wx.ICON_WARNING)== wx.YES):
                self.startSettings(wx.Event)
                self.pause()
                return
                    
        t = threading.Thread(target=b.start_playing, args=())
        t.daemon = True
        slider = threading.Thread(target=self.updateSlider, args=())
        slider.daemon = True
        try:
            t.start()
        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread()
            sys.exit()
        while(b.paused):
            time.sleep(1)
            print("waiting to play")
        # might need to wait here
        try:
            slider.start()
        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread()
            sys.exit()
        self.m_listCtrl1.SetItemImage(b.num_in_q, self.imglistdict[1])
        self.m_listCtrl1.SetItemBackgroundColour(
            b.num_in_q, wx.Colour("yellow"))
        self.currentSong.SetLabel(str(b.r.currentTrack.get("trackName")))
        self.currentArtist.SetLabel(str(b.r.currentTrack.get("artistName")))
        self.currentAlbum.SetLabel(str(b.r.currentTrack.get("albumName")))
        self.fgSizer1.Layout()

    def changeSlider(self,event):
        print("Click!")
        order=["song","total_time","total_songs"]
        place=order.index(self.slider)
        if place < len(order)-1:
            place+=1
        else:
            place=0
        self.slider=order[place]
    def alreadyWritten(self):
        urls = ['pubads.g.doubleclick.net', 'securepubads.g.doubleclick.net',
                'www.googletagservices.com', 'gads.pubmatic.com', 'ads.pubmatic.com', 'spclient.wg.spotify.com']
        str = "\n"
        for u in urls:
            str += '0.0.0.0 ' + u + "\n"

        try:
            path = os.environ.get('windir') + "\\System32\\drivers\\etc\\hosts"

            if str in open(path).read():
                return True
        except:
            pass
        return False

    def removeAds(self, event):
        if self.alreadyWritten():
            wx.MessageBox("You already have ads removed",
                          "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            if wx.MessageBox('This experimental feature removes ads by modifying the hosts file.\n'+
                            'Which then points the domains used for adversitments to empty IPs\n'+
                            'Admin privlidges are required for this to run.\n\nContinue?', 
                            'Remove Ads', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION) == wx.YES:
                # Re-run the program with admin rights
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", 'addRemover.exe', '', None, 1)
                time.sleep(1)
                if self.alreadyWritten():
                    wx.MessageBox("Success\nRestart Spotify to remove ads",
                                  "Success", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("Unable to edit hosts file",
                                  "Error", wx.OK | wx.ICON_INFORMATION)

    def updateSlider(self):
        slept = 0
        while not b.k.get("playing"):
            time.sleep(1)  # ghetto but we need to wait for things to start
            slept += 1
        total_len = int(b.r.currentTrack.get("trackLength"))
        urllib.request.urlretrieve(
            b.r.currentTrack["albumCover"], "temp_album.jpg")
        image = wx.Bitmap.ConvertToImage(
            wx.Bitmap("temp_album.jpg", wx.BITMAP_TYPE_ANY))
        image = image.Scale(50, 50, wx.IMAGE_QUALITY_HIGH)
        self.m_bitmap1.SetBitmap(wx.Bitmap(image))
        self.currentSong.SetLabel(str(b.r.currentTrack.get("trackName")))
        self.currentArtist.SetLabel(str(b.r.currentTrack.get("artistName")))
        self.currentAlbum.SetLabel(str(b.r.currentTrack.get("albumName")))
        
        self.fgSizer1.Layout()  # re-center
        start_time = time.time()
        song_num = b.num_in_q
        value = 0
        left_string="0:00"
        right_string="0:00"
        while b.k.get('playing') and (not b.paused):
            if self.slider=='total_time':
                left_string=str(datetime.timedelta(seconds=(time.time() - start_time + 1 +b.recorded_secs)))[2:7]
                right_string = str(datetime.timedelta(seconds=(b.total_secs)))[2:7]
                value=int(100*(time.time() - start_time + 1 +b.recorded_secs)/b.total_secs)
            elif self.slider=='total_songs':
                left_string=str(b.num_in_q)
                right_string=str(len(b.song_queue))
                value=int(100*(b.num_in_q)/len(b.song_queue))
            elif self.slider=='song':
                right_string=str(datetime.timedelta(seconds=total_len))[2:7]
                value = int(100 * (time.time() - start_time + slept) / total_len)
                left_string=str(datetime.timedelta(seconds=(time.time() - start_time + 1)))[2:7]
            self.left_status.SetLabel(left_string)
            self.right_status.SetLabel(right_string)
            self.m_gauge1.SetValue(value)
            # print("playing",value)
            time.sleep(1)
            if value > 100 and (b.k.get('playing') is False) and b.song_queue[song_num]['status'] == 'complete':
                # we are done
                self.songOver()
                return
        if value > 70 and b.song_queue[song_num]['status'] == 'complete':
            self.songOver()
        else:
            if not b.paused:
                print("Gui thinks ad?")
                self.updateSlider()  # we had an add so we need to restart

    def songOver(self):
        print("Num in Q", b.num_in_q)
        if (b.num_in_q > 0):
            self.m_listCtrl1.SetItemBackgroundColour(
                b.num_in_q - 1, wx.Colour("green"))
            self.m_listCtrl1.SetItemImage(b.num_in_q - 1, self.imglistdict[2])
            print("q", b.num_in_q, "len=", len(b.song_queue))
            if b.num_in_q < len(b.song_queue):
                self.m_listCtrl1.SetItemBackgroundColour(
                    b.num_in_q, wx.Colour("yellow"))
                self.m_listCtrl1.SetItemImage(b.num_in_q, self.imglistdict[1])

                slider = threading.Thread(target=self.updateSlider, args=())
                slider.daemon = True
                try:
                    slider.start()
                except (KeyboardInterrupt, SystemExit):
                    cleanup_stop_thread()
                    sys.exit()
            if b.num_in_q == len(b.song_queue):
                self.m_listCtrl1.SetItemBackgroundColour(
                    b.num_in_q - 1, wx.Colour("green"))
                self.m_listCtrl1.SetItemImage(
                    b.num_in_q - 1, self.imglistdict[2])
                self.endOfQ()
                if wx.MessageBox('Queue Completed\nDo you want to clear the Queue?', 'Done Recording', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION) == wx.YES:
                    self.clearQueue(None)
                b.num_in_q = -1

# however it does add give the loading screen
    def updateQ(self):

        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        if(os.path.isfile(b.filename)):
            with open(b.filename) as f:
                b.list_of_songs = f.readlines()

            if(b.list_of_songs != None):
                for song in b.list_of_songs:
                    tmp = b.getTrackInfo(
                        (song.lstrip("https://open.spotify.com/track/")).rstrip('\n'))
                    self.addItemtoQ(tmp)
        else:
            # file does not exist need to find graceful way to stop
            print("no file bruh")
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        
    def addItemtoQ(self, entry):
        b.total_secs+=int(entry.get("trackLength"))
        b.song_queue.append(entry)
        pos = self.m_listCtrl1.GetItemCount()

        x = self.m_listCtrl1.InsertItem(
            pos, entry.get("trackName"), self.imglistdict[0])

        self.m_listCtrl1.SetItem(pos, 1, entry.get("artistName"))
        self.m_listCtrl1.SetItem(pos, 2, entry.get("albumName"))
        self.m_listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.m_listCtrl1.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.m_listCtrl1.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.m_listCtrl1.Update()

    def clearQueue(self, event):
        self.m_listCtrl1.DeleteAllItems()
        self.m_listCtrl1.Update()
        b.num_in_q = -1
        b.list_of_songs = []
        b.song_queue = []

    def moveSelectionUp(self, event):
        current = self.m_listCtrl1.GetFirstSelected()
        if current > b.num_in_q + 1 or (current == b.num_in_q and "Play" in str(self.status)):
            b.song_queue[current], b.song_queue[current -
                                                1] = b.song_queue[current - 1], b.song_queue[current]
            data = []
            for i in range(3):
                data.append(self.m_listCtrl1.GetItemText(current, i))
            self.m_listCtrl1.InsertItem(current - 1, data[0])
            self.m_listCtrl1.SetItem(current - 1, 1, data[1])
            self.m_listCtrl1.SetItem(current - 1, 2, data[2])
            self.m_listCtrl1.DeleteItem(current + 1)
            self.m_listCtrl1.Select(current - 1)

    def moveSelectionDown(self, event):
        current = self.m_listCtrl1.GetFirstSelected()
        if (current > b.num_in_q or (current == b.num_in_q and "Play" in str(self.status))) and current < len(b.song_queue) - 1:
            b.song_queue[current], b.song_queue[current +
                                                1] = b.song_queue[current + 1], b.song_queue[current]
            data = []
            for i in range(3):
                data.append(self.m_listCtrl1.GetItemText(current, i))
            self.m_listCtrl1.InsertItem(current + 2, data[0])
            self.m_listCtrl1.SetItem(current + 2, 1, data[1])
            self.m_listCtrl1.SetItem(current + 2, 2, data[2])
            self.m_listCtrl1.DeleteItem(current)
            self.m_listCtrl1.Select(current + 1)
            
    def deleteSelection(self, event):
        current = self.m_listCtrl1.GetFirstSelected()
        while current != -1:
            if current > b.num_in_q or (current == b.num_in_q and "Play" in str(self.status)):
                b.total_secs-=b.song_queue[current].get("trackLength")
                del b.song_queue[current]
                self.m_listCtrl1.DeleteItem(current)
                current = self.m_listCtrl1.GetFirstSelected()
            else:
                if current == b.num_in_q:
                    dlg = wx.MessageBox("You cannot delete songs that are currently being played",
                                        "Cannot Delete",     wx.OK | wx.ICON_INFORMATION)
                elif current < b.num_in_q:
                    dlg = wx.MessageBox("You cannot delete songs that have already been played",
                                        "Cannot Delete",  wx.OK | wx.ICON_INFORMATION)
                current = -1

    def loadingWorker(self):
        lengthy = len(b.song_queue)
        progressMax = len(b.list_of_songs)
        print(progressMax, lengthy)
        while lengthy < progressMax:
            time.sleep(.5)
            lengthy = len(b.song_queue)
            wx.CallAfter(pub.sendMessage, "update", msg=str(lengthy))

    def openDir(self, dir):
        cmd = "explorer.exe " + dir
        os.system(cmd)

    def changeSaveAs(self, event):
        dlg = wx.DirDialog(
            None,
            "Save files in ...",
            defaultPath=b.r.saveAs,
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.DD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            b.r.saveAs = dlg.GetPath()
        dlg.Destroy()
        print(b.r.saveAs)
        # check that there are no conflicts with the new location
        for entry in b.song_queue:
            if(os.path.isfile(b.r.saveAs + "\\" + entry.get("fileName") + ".mp3")):
                result = wx.MessageBox('Found matching file\n' + entry.get("fileName") + '.mp3\nDo you want to overwrite this?',
                                       'File Conflict', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION)
                if(result is wx.NO):
                    itm = self.m_listCtrl1.FindItem(0, entry.get("trackName"))
                    self.m_listCtrl1.DeleteItem(itm)
                    b.song_queue.remove(entry)
                    self.m_listCtrl1.Update()

    def changeFile(self, event):
        print(self.m_filePicker1.GetPath())
        b.filename = self.m_filePicker1.GetPath()
        self.updateQ()

    def startSettings(self, event):
        s = SettingsDialog(self, b, b.r.audioList, b.r.device_id,
                           b.r.bitrate, b.filename, b.paused)
        t=threading.Thread(target=s.volumeLoop, args=())
        t.start()
        s.Show()
        s.save.Bind(wx.EVT_BUTTON, lambda evt,
                    temp=s: self.saveSettings(evt, temp))

    def saveSettings(self, evt, temp):
        b.r.device_id = int(temp.m_choice1.GetCurrentSelection())
        print("Audio id:", b.r.device_id)
        b.r.recordingSetup()

        b.filename = temp.m_filePicker1.GetPath()
        b.r.bitrate = temp.bitrate.GetStringSelection()
        print("Bitrate:", b.r.bitrate)
        temp.open = False
        temp.Destroy()
        # update the queue
        self.updateQ()

    def endOfQ(self):
        self.pause()

    def playOrPause(self, event):
        if "pause" in str(self.status):
            self.pause()
        else:
            self.play()

    def pause(self):
        self.m_bpButton1.SetBitmapLabel(
            wx.Bitmap(b.r.cwd + "\\play.bmp", wx.BITMAP_TYPE_ANY))
        self.status = 'Play'
        self.m_bpButton2.Enable(True)
        self.m_button2.Enable(True)
        self.m_menuItem1.Enable(True)
        self.currentSong.SetLabel("")
        self.right_status.SetLabel("0:00")
        self.left_status.SetLabel("0:00")
        self.currentArtist.SetLabel("Not Recording")
        self.currentAlbum.SetLabel("")
        self.m_bitmap1.SetBitmap(wx.Bitmap())
        self.bSizer2.Layout()
        b.paused = True
        if b.num_in_q < self.m_listCtrl1.GetItemCount() and b.num_in_q > 0:
            self.m_listCtrl1.SetItemBackgroundColour(
                b.num_in_q, wx.Colour("white"))
            self.m_listCtrl1.SetItemImage(b.num_in_q, self.imglistdict[0])
        pauser = threading.Thread(target=b.pause, args=())
        pauser.daemon = True
        try:
            pauser.start()
        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread()
            sys.exit()
        self.m_gauge1.SetValue(0)

    def audioSwap(self, event):
        b.r.device_id = int(self.m_choice1.GetCurrentSelection())
        print(b.r.device_id)
        b.r.recordingSetup()
    def checkVersion(self):
        latest_url='https://github.com/ailgup/Recordify/releases/latest'
        result=urllib.request.urlopen(latest_url)
        final=result.geturl().split("/")[-1].split(".")
        split_version = VERSION.split(".")
        if (final[0]>split_version[0] or (final[0]==split_version[0] and final[1]>split_version[1])) and VERSION!="0.0":
            if wx.MessageBox('There is an update to Recordify!\n\nDownload now?','Update Available',wx.YES_NO) == wx.YES:
                webbrowser.open(latest_url)
    def OnAboutBox(self, e):

        description = """Recordify is a free program which records music played\non Spotify and saves it for future playback in a MP3 format."""
        licence = """DO NOT DISTIBUTE COPYWRITTEN MUSIC RECORDED USING RECORDIFY.\nDoing so is illegal."""
        info = wx.adv.AboutDialogInfo()
        info.SetIcon(wx.Icon('rec_50px.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Recordify')
        info.SetVersion(str(VERSION))
        info.SetDescription(description)
        info.SetCopyright('(C) 2017 Chris Puglia')
        info.SetWebSite('https://github.com/ailgup/Recordify')
        info.SetLicence(licence)
        info.AddDeveloper('Chris Puglia')
        wx.adv.AboutBox(info)

    def __del__(self):
        pass

if __name__ == "__main__":
    # Icons() #makes the icons
    b = Backend()
    app = wx.App(False)
    locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    tries=2
    while tries>0:
        try:
            b.start()
            break
        except OSError:
            #temp debug
            #raise
            tries-=1
            if (tries > 0):
                dial = wx.MessageDialog(
                    None, 'Unable to connect.\nMake sure you have Spotify running, and you have an internet connection', 'Error', wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
                quit()
    icon = wx.Icon()
    icon.CopyFromBitmap(wx.Bitmap("rec_50px.png", wx.BITMAP_TYPE_ANY))

    frame = Recordify(parent=None)
    frame.SetIcon(icon)
    frame.Show()

    app.MainLoop()
