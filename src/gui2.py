# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Jun 17 2015)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import threading
import time
import os
from wx.lib.pubsub import pub
import base64
from recorder import Backend
from SettingsDialog import SettingsDialog
# from DebugFrame import DebugFrame
from Loading import Loading
from icons import Icons
###########################################################################
# Class Recordify
###########################################################################
########################################################################


class MyProgressDialog(wx.Dialog):
    """"""
    #----------------------------------------------------------------------

    def __init__(self, max=100):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Progress")
        self.count = 0
        self.max = max
        self.progress = wx.Gauge(self, range=self.max)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update")
    #----------------------------------------------------------------------

    def updateProgress(self, msg):
        """"""
        self.count = int(msg)
        print("count:", self.count, " max:", self.max)
        if self.count >= self.max:
            self.Destroy()
        self.progress.SetValue(self.count)
########################################################################


class MyURLDropTarget(wx.PyDropTarget):

    #----------------------------------------------------------------------
    def __init__(self, window):
        wx.DropTarget.__init__(self)
        self.window = window

        self.data = wx.URLDataObject()
        self.SetDataObject(self.data)

    #----------------------------------------------------------------------
    def OnDragOver(self, x, y, d):
        return wx.DragLink

    #----------------------------------------------------------------------
    def OnData(self, x, y, d):
        if not self.GetData():
            return wx.DragNone
        url = self.data.GetURL()

        self.window.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        for line in url.split('\n'):
            if("https://open.spotify.com/track/" in url):
                tmp = b.getTrackInfo(
                    (line.lstrip("https://open.spotify.com/track/")).rstrip('\n'))
                # b.song_queue.append(tmp)
                frame.addItemtoQ(tmp)
                #frame.index += 1
                # print(len(b.song_queue))
            #self.window.AppendText(url + "\n")

            else:
                wx.MessageBox(
                    "This is not a Spotify Song\n\nTo use properly drag a song, or many songs, over from the Spotify application", "Error", wx.OK | wx.ICON_ERROR)
        self.window.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        return d


from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class ResizeListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(
            self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        ListCtrlAutoWidthMixin.__init__(self)


class Recordify (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Recordify", pos=wx.DefaultPosition,
                          size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        ####
        gSizer5 = wx.GridSizer(0, 2, 0, 0)

        self.fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        self.fgSizer1.SetFlexibleDirection(wx.HORIZONTAL)
        self.fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        self.m_bpButton1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(
            "play.bmp"), wx.DefaultPosition, (58, 58), wx.BU_AUTODRAW | wx.DOUBLE_BORDER)
        #self.m_bpButton1.SetBitmapCurrent( wx.Bitmap( "play2.bmp") )
        self.fgSizer1.Add(self.m_bpButton1, 0, wx.ALL, 5)

        self.bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.currentSong = wx.StaticText(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.currentSong.Wrap(-1)
        self.bSizer2.Add(self.currentSong, 0, wx.ALL, 3)

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
            "folder.bmp", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)

        self.m_bpButton2.SetBitmapCurrent(
            wx.Bitmap("folder2.bmp", wx.BITMAP_TYPE_ANY))
        gSizer5.Add(self.m_bpButton2, 0, wx.ALL |
                    wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer5.Add(gSizer5, 1, wx.EXPAND, 5)

        #####
        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_gauge1 = wx.Gauge(
            self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(-1, -1), wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(0)
        bSizer4.Add(self.m_gauge1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        bSizer5.Add(bSizer4, 0, wx.EXPAND, 5)

        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        self.m_listCtrl1 = ResizeListCtrl(self)

        self.m_listCtrl1.SetToolTip(
            u"Drag songs here from the Spotify application")
        self.m_listCtrl1.InsertColumn(0, 'Name')
        self.m_listCtrl1.InsertColumn(1, 'Artist')
        self.m_listCtrl1.InsertColumn(2, 'Album')

        # self.m_listCtrl1.setResizeColumn(0)
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
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Settings", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)

        self.m_menuItem2 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem2)

        self.m_menuItem4 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Debug", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem4)

        self.m_menu1.AppendSeparator()

        self.m_menuItem3 = wx.MenuItem(
            self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem3)

        self.m_menubar1.Append(self.m_menu1, u"File")

        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.BOTH)
        #####################
        # Stuff added by hand
        #####################

        self.index = 0
        self.Bind(wx.EVT_MENU, self.startSettings, self.m_menuItem1)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, self.m_menuItem2)
        # self.Bind(wx.EVT_MENU, self.openDebug,self.m_menuItem4)
        self.m_button1.Bind(wx.EVT_BUTTON, self.deleteSelection)
        self.m_button2.Bind(wx.EVT_BUTTON, self.clearQueue)  # must write
        self.m_bpButton1.Bind(wx.EVT_BUTTON, self.playOrPause)
        self.m_bpButton2.Bind(wx.EVT_BUTTON, self.changeSaveAs)
        dt = MyURLDropTarget(self.m_listCtrl1)
        self.m_listCtrl1.SetDropTarget(dt)
        self.status = "play"
# Connect Events

    def play(self):
        self.m_bpButton1.SetBitmapLabel(
            wx.Bitmap(b.r.cwd + "\\pause.bmp", wx.BITMAP_TYPE_ANY))
        #self.m_bpButton1.SetBitmapCurrent( wx.Bitmap("pause2.bmp", wx.BITMAP_TYPE_ANY ) )
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

        self.m_listCtrl1.SetItemBackgroundColour(
            b.num_in_q, wx.Colour("yellow"))
        self.currentSong.SetLabel(str(b.r.currentTrack.get("trackName")))
        self.currentArtist.SetLabel(str(b.r.currentTrack.get("artistName")))
        self.currentAlbum.SetLabel(str(b.r.currentTrack.get("albumName")))
        self.fgSizer1.Layout()

    def updateSlider(self):
        import time
        slept = 0
        while not b.k.get("playing"):
            time.sleep(1)  # ghetto but we need to wait for things to start
            slept += 1
        self.currentSong.SetLabel(str(b.r.currentTrack.get("trackName")))
        self.currentArtist.SetLabel(str(b.r.currentTrack.get("artistName")))
        self.currentAlbum.SetLabel(str(b.r.currentTrack.get("albumName")))
        self.fgSizer1.Layout()  # re-center
        start_time = time.time()
        total_len = int(b.r.currentTrack.get("trackLength"))
        value = 0
        while b.k.get('playing') and (not b.paused):
            value = int(100 * (time.time() - start_time + slept) / total_len)
            self.m_gauge1.SetValue(value)
            print("playing", value)
            time.sleep(1)
            if value > 100 and (b.k.get('playing') is False):
                # we are done
                self.songOver()
                return
        if value > 70:
            self.songOver()
        else:
            if not b.paused:
                print("Gui thinks ad?")
                self.updateSlider()  # we had an add so we need to restart
        print("leaving so soon", value)

    def songOver(self):
        print("Num in Q", b.num_in_q)
        #top = self.m_listCtrl1.GetItemData(b.num_in_q)
        self.m_listCtrl1.SetItemBackgroundColour(
            b.num_in_q - 1, wx.Colour("green"))
        print("q", b.num_in_q, "len=", len(b.song_queue))
        if b.num_in_q < len(b.song_queue):
            self.m_listCtrl1.SetItemBackgroundColour(
                b.num_in_q, wx.Colour("yellow"))
            print("ya")
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
            self.endOfQ()
            if wx.MessageBox('Queue Completed\nDo you want to clear the Queue?', 'Done Recording', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION) == wx.YES:
                del b.song_queue[:]
                print("q:", b.song_queue)
                while self.m_listCtrl1.GetItemCount() > 0:
                    self.m_listCtrl1.DeleteItem(0)
                    self.m_listCtrl1.Update()
            b.num_in_q = -1

# however it does add give the loading screen
    def updateQ(self):
        # b.song_queue=[]
        # b.list_of_songs=[]
        # self.m_listCtrl1.ClearAll()
        # self.m_listCtrl1.InsertColumn(0, 'Name')
        # self.m_listCtrl1.InsertColumn(1, 'Artist')
        # self.m_listCtrl1.InsertColumn(2, 'Album', width=125)
        # self.index=0
        #####
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        # loading = threading.Thread(target=self.loadingWorker, args=())
        # loading.daemon = True
        # loading2 = threading.Thread(target=b.createQ, args=())
        # loading2.daemon = True
        # try:
        # loading2.start()
        # loading.start()
        # except (KeyboardInterrupt, SystemExit):
        # cleanup_stop_thread();
        # sys.exit()
        # added
        print("yo")
        if(os.path.isfile(b.filename)):
            with open(b.filename) as f:
                b.list_of_songs = f.readlines()

            if(b.list_of_songs != None):
                for song in b.list_of_songs:
                    tmp = b.getTrackInfo(
                        (song.lstrip("https://open.spotify.com/track/")).rstrip('\n'))
                    self.addItemtoQ(tmp)
                    # self.song_queue.append([tmp.get("trackName"),tmp.get("artistName"),tmp.get("albumName")])
                    # print(tmp.get("trackName"))
        else:
            # file does not exist need to find graceful way to stop
            print("no file bruh")
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        # while(len(b.list_of_songs)==0):
        #	time.sleep(1) #waiting to populate
        #progressMax = len(b.list_of_songs)
        #print (progressMax)
        #dlg = MyProgressDialog(max=progressMax)
        # dlg.ShowModal()

        # end added
        # b.createQ()

    def addItemtoQ(self, entry):
        add = True
        if(os.path.isfile(b.r.saveAs + "\\" + entry.get("fileName") + ".mp3")):
            result = wx.MessageBox('Found matching file\n' + entry.get("fileName") + '.mp3\nDo you want to overwrite this?',
                                   'File Conflict', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION)
            if(result is wx.NO):
                add = False
        if(add):
            b.song_queue.append(entry)
            pos = self.m_listCtrl1.GetItemCount()
            x = self.m_listCtrl1.InsertItem(pos, entry.get("trackName"))
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

    def deleteSelection(self, event):
        current = self.m_listCtrl1.GetFirstSelected()
        while current != -1:
            if current > b.num_in_q or (current == b.num_in_q and "Play" in str(self.status)):
                name = str(self.m_listCtrl1.GetItemText(current))
                for item in b.song_queue:
                    if item.get("trackName") == name:
                        b.song_queue.remove(item)
                        #print("Song Removed",b.song_queue)
                self.m_listCtrl1.DeleteItem(current)
                current = self.m_listCtrl1.GetFirstSelected()
            else:
                if current == b.num_in_q:
                    dlg = wx.MessageBox("You cannot delete songs that are currently being played",
                                        "Cannot Delete",	 wx.OK | wx.ICON_INFORMATION)
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
                    print(itm)
                    self.m_listCtrl1.DeleteItem(itm)
                    b.song_queue.remove(entry)
                    self.m_listCtrl1.Update()

    def changeFile(self, event):
        print(self.m_filePicker1.GetPath())
        b.filename = self.m_filePicker1.GetPath()
        self.updateQ()

    def startSettings(self, event):
        s = SettingsDialog(self, b.r.audioList, b.r.device_id,
                           b.r.bitrate, b.filename, b.paused)
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
        temp.Destroy()
        # update the queue
        self.updateQ()
        # print("Filename:",b.filename)
        # if(os.path.isfile(b.filename)):

        # import multiprocessing
        # dia = wx.Dialog(parent=self, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL, name="Progress")
        # loading = threading.Thread(target=dia.Show, args=())
        # loading.daemon = True
        # loading.start()

        # with open(b.filename) as f:
        # b.list_of_songs = f.readlines()
        # if(b.list_of_songs!=None):
        # for song in b.list_of_songs:
        # if("https://open.spotify.com/track/" in song):
        # tmp = b.getTrackInfo((song.lstrip("https://open.spotify.com/track/")).rstrip('\n'))
        # b.song_queue.append(tmp)
        # frame.addItemtoQ(tmp)
        ##frame.index += 1
        # print(len(b.song_queue))
        ###self.window.AppendText(url + "\n")
        # else:
        # wx.MessageBox("This is not a Spotify Song\n\nTo use properly drag a song, or many songs, over from the Spotify application","Error",wx.OK|wx.ICON_ERROR)
        # dia.Destroy()

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
        #self.m_bpButton1.SetBitmapCurrent( wx.Bitmap("play2.bmp", wx.BITMAP_TYPE_ANY ) )
        self.status = 'Play'
        self.m_bpButton2.Enable(True)
        self.m_button2.Enable(True)
        self.m_menuItem1.Enable(True)
        self.currentSong.SetLabel("")
        self.currentArtist.SetLabel("Not Recording")
        self.currentAlbum.SetLabel("")
        self.bSizer2.Layout()
        b.paused = True
        if b.num_in_q < self.m_listCtrl1.GetItemCount():
            self.m_listCtrl1.SetItemBackgroundColour(
                b.num_in_q, wx.Colour("white"))
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

    def OnAboutBox(self, e):
        wx.MessageBox('Recordify v1.1\n\n(C) 2016 \n\nRecordify is a free program which records music played\non Spotify and saves it for future playback in a MP3 format.\nDO NOT DISTIBUTE COPYWRITTEN MUSIC RECORDED USING RECORDIFY.\nDoing so is illegal.',
                      "Info",
                      wx.OK | wx.ICON_INFORMATION)

        # info.SetIcon()
        # info.SetName('Recordify')
        # info.SetVersion('1.0')
        # info.SetDescription(description)
        # info.SetCopyright('(C) 2016 ')
        # info.SetLicence(licence)
        # wx.adv.AboutBox(info)
    # def openDebug(self,event):
        # t = threading.Thread(target=DebugFrame, args=(self,))
        # t.daemon = True
        # t.start()

    def __del__(self):
        pass


if __name__ == "__main__":
    Icons()  # makes the icons
    b = Backend()
    app = wx.App(False)
    #locale = wx.Locale(wx.LANGUAGE_ENGLISH)

    try:
        b.start()
    except OSError:
        raise
        dial = wx.MessageDialog(
            None, 'Unable to connect.\nMake sure you have Spotify running, and you have an internet connection', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        quit()
    icon = wx.Icon()
    #info = wx.adv.AboutDialogInfo()
    ico1_b64 = \
        """
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
"""
# convert back to binary to save it
    ico1 = base64.b64decode(ico1_b64)
    fout = open("recordify.ico", "wb")
    fout.write(ico1)
    fout.close()
    icon.CopyFromBitmap(wx.Bitmap("recordify.ico", wx.BITMAP_TYPE_ANY))

    frame = Recordify(parent=None)
    frame.SetIcon(icon)
    frame.Show()

    app.MainLoop()
