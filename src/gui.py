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
from Loading import Loading
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
                b.song_queue.append(tmp)
                frame.addItemtoQ(tmp)
                #frame.index += 1
                # print(len(b.song_queue))
            #self.window.AppendText(url + "\n")

            else:
                wx.MessageBox(
                    "This is not a Spotify Song\n\nTo use properly drag a song, or many songs, over from the Spotify application", "Error", wx.OK | wx.ICON_ERROR)
        self.window.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        return d


class Recordify (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Recordify", pos=wx.DefaultPosition,
                          size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.m_menubar1 = wx.MenuBar(0)

        self.settings = wx.Menu()
        self.settings_item = self.settings.Append(
            wx.NewId(), 'Settings', "Settings")
        self.m_menubar1.Append(self.settings, u"Settings")

        self.about = wx.Menu()
        self.about_item = self.about.Append(wx.ID_ABOUT, 'Info', 'App Info')
        self.m_menubar1.Append(self.about, u"About")

        self.Bind(wx.EVT_MENU, self.startSettings, self.settings_item)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, self.about_item)

        self.SetMenuBar(self.m_menubar1)

        gSizer3 = wx.GridSizer(1, 2, 0, 0)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(
            self, wx.ID_ANY, u"Queue", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(
            wx.Font(15, 70, 90, 90, False, wx.EmptyString))

        bSizer8.Add(self.m_staticText2, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL, 5)

        #####
        self.m_listCtrl2 = wx.ListCtrl(
            self, size=(-1, 100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.m_listCtrl2.SetToolTip(
            u"Drag songs here from the Spotify application")
        self.m_listCtrl2.InsertColumn(0, 'Name')
        self.m_listCtrl2.InsertColumn(1, 'Artist')
        self.m_listCtrl2.InsertColumn(2, 'Album')
        self.index = 0
        ###

        bSizer8.Add(self.m_listCtrl2, 1, wx.ALL | wx.EXPAND, 5)

        gSizer3.Add(bSizer8, 1, wx.EXPAND, 5)

        gSizer4 = wx.GridSizer(2, 1, 0, 0)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(
            self, wx.ID_ANY, u"Select Audio Output", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer10.Add(self.m_staticText5, 0, wx.ALL |
                     wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_choice1Choices = b.r.audioList
        self.m_choice1 = wx.Choice(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        bSizer10.Add(self.m_choice1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText6 = wx.StaticText(
            self, wx.ID_ANY, u"Select Output Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        bSizer10.Add(self.m_staticText6, 0, wx.ALL |
                     wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_dirPicker2 = wx.DirPickerCtrl(
            self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        bSizer10.Add(self.m_dirPicker2, 0, wx.ALL |
                     wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.m_dirPicker2.SetPath(b.r.saveAs)

        self.m_staticText7 = wx.StaticText(
            self, wx.ID_ANY, u"List", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        bSizer10.Add(self.m_staticText7, 0, wx.ALL |
                     wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_filePicker1 = wx.FilePickerCtrl(
            self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        bSizer10.Add(self.m_filePicker1, 0, wx.ALL |
                     wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer4.Add(bSizer10, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText3 = wx.StaticText(
            self, wx.ID_ANY, u"Now Playing", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetFont(
            wx.Font(15, 70, 90, 90, False, wx.EmptyString))

        self.bSizer11.Add(self.m_staticText3, 0, wx.ALL |
                          wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.deleteSelectionButton = wx.Button(
            self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer11.Add(self.deleteSelectionButton, 0,
                          wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, u"Play", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer11.Add(self.m_button1, 0, wx.ALL |
                          wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText4 = wx.StaticText(
            self, wx.ID_ANY, u"Nothing Playing Now", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        self.bSizer11.Add(self.m_staticText4, 0, wx.ALL |
                          wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_gauge1 = wx.Gauge(
            self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(0)
        self.bSizer11.Add(self.m_gauge1, 0, wx.ALL | wx.EXPAND, 5)

        gSizer4.Add(self.bSizer11, 1, wx.EXPAND, 5)

        gSizer3.Add(gSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(gSizer3)
        self.Layout()
        gSizer3.Fit(self)

        self.Centre(wx.BOTH)
        self.deleteSelectionButton.Bind(wx.EVT_BUTTON, self.deleteSelection)
        self.m_button1.Bind(wx.EVT_BUTTON, self.playOrPause)
        self.Bind(wx.EVT_DIRPICKER_CHANGED,
                  self.changeSaveAs, self.m_dirPicker2)
        self.Bind(wx.EVT_FILEPICKER_CHANGED,
                  self.changeFile, self.m_filePicker1)
        self.m_choice1.Bind(wx.EVT_CHOICE, self.audioSwap)
        dt = MyURLDropTarget(self.m_listCtrl2)
        self.m_listCtrl2.SetDropTarget(dt)
# Connect Events

    def play(self):
        self.m_button1.SetLabel('Pause')
        self.m_filePicker1.Enable(False)
        self.m_dirPicker2.Enable(False)
        self.m_choice1.Enable(False)
        if(len(b.song_queue) is 0):

            print("No songs in Q!")
            wx.MessageBox('There are no songs in the queue!\nDrag song(s) from the Spotify application to the app.',
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

        self.m_listCtrl2.SetItemBackgroundColour(
            b.num_in_q, wx.Colour("yellow"))
        self.m_staticText4.SetLabel(str(b.r.currentTrack.get(
            "trackName")) + " - " + str(b.r.currentTrack.get("artistName")))
        self.bSizer11.Layout()

    def updateSlider(self):
        import time
        slept = 0
        while not b.k.get("playing"):
            time.sleep(1)  # ghetto but we need to wait for things to start
            slept += 1
        self.m_staticText4.SetLabel(str(b.r.currentTrack.get(
            "trackName")) + " - " + str(b.r.currentTrack.get("artistName")))
        self.bSizer11.Layout()  # re-center
        start_time = time.time()
        total_len = int(b.r.currentTrack.get("trackLength"))
        value = 0
        while b.k.get('playing') and (not b.paused):
            value = int(100 * (time.time() - start_time + slept) / total_len)
            self.m_gauge1.SetValue(value)
            time.sleep(1)
        if value > 70:
            self.songOver()
        else:
            if not b.paused:
                print("Gui thinks ad?")
                self.updateSlider()  # we had an add so we need to restart
        print("leaving so soon", value)

    def songOver(self):
        print("Num in Q", b.num_in_q)
        #top = self.m_listCtrl2.GetItemData(b.num_in_q)
        self.m_listCtrl2.SetItemBackgroundColour(
            b.num_in_q - 1, wx.Colour("green"))
        print("q", b.num_in_q, "len=", len(b.song_queue))
        if b.num_in_q < len(b.song_queue):
            self.m_listCtrl2.SetItemBackgroundColour(
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
            self.m_listCtrl2.SetItemBackgroundColour(
                b.num_in_q - 1, wx.Colour("green"))
            self.endOfQ()
            if wx.MessageBox('Queue Completed\nDo you want to clear the Queue?', 'Done Recording', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION) == wx.YES:
                del b.song_queue[:]
                print("q:", b.song_queue)
                while self.m_listCtrl2.GetItemCount() > 0:
                    self.m_listCtrl2.DeleteItem(0)
                    self.m_listCtrl2.Update()
            b.num_in_q = -1

# however it does add give the loading screen
    def updateQ(self):
        # b.song_queue=[]
        # b.list_of_songs=[]
        # self.m_listCtrl2.ClearAll()
        # self.m_listCtrl2.InsertColumn(0, 'Name')
        # self.m_listCtrl2.InsertColumn(1, 'Artist')
        # self.m_listCtrl2.InsertColumn(2, 'Album', width=125)
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
                    print("adding")
                    self.addItemtoQ(tmp)
                    print("added")
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
                b.song_queue.remove(entry)
        if(add):
            b.song_queue.append(entry)
            pos = self.m_listCtrl2.GetItemCount()
            x = self.m_listCtrl2.InsertItem(pos, entry.get("trackName"))
            self.m_listCtrl2.SetItem(pos, 1, entry.get("artistName"))
            self.m_listCtrl2.SetItem(pos, 2, entry.get("albumName"))
            self.m_listCtrl2.Update()

    def deleteSelection(self, event):
        current = self.m_listCtrl2.GetFirstSelected()
        while current != -1 and (current > b.num_in_q):
            name = str(self.m_listCtrl2.GetItemText(current))
            for item in b.song_queue:
                if item.get("trackName") == name:
                    b.song_queue.remove(item)
                    # print(b.song_queue)
            self.m_listCtrl2.DeleteItem(current)
            current = self.m_listCtrl2.GetFirstSelected()

    def loadingWorker(self):
        print("eee")

        lengthy = len(b.song_queue)
        progressMax = len(b.list_of_songs)
        print(progressMax, lengthy)
        while lengthy < progressMax:
            print("entered")
            time.sleep(.5)
            lengthy = len(b.song_queue)
            print("lengthening")
            wx.CallAfter(pub.sendMessage, "update", msg=str(lengthy))

    def changeSaveAs(self, event):
        print(self.m_dirPicker2.GetPath())
        b.r.saveAs = self.m_dirPicker2.GetPath()
        # check that there are no conflicts with the new location
        for entry in b.song_queue:
            if(os.path.isfile(b.r.saveAs + "\\" + entry.get("fileName") + ".mp3")):
                result = wx.MessageBox('Found matching file\n' + entry.get("fileName") + '.mp3\nDo you want to overwrite this?',
                                       'File Conflict', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION)
                if(result is wx.NO):
                    itm = self.m_listCtrl2.FindItem(0, entry.get("trackName"))
                    print(itm)
                    self.m_listCtrl2.DeleteItem(itm)
                    b.song_queue.remove(entry)
                    self.m_listCtrl2.Update()

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
        print(self.m_button1.GetLabel())
        if "Pause" in str(self.m_button1.GetLabel()):
            self.pause()
        else:
            self.play()

    def pause(self):
        self.m_button1.SetLabel('Play')
        self.m_filePicker1.Enable(True)
        self.m_dirPicker2.Enable(True)
        self.m_choice1.Enable(True)
        self.m_staticText4.SetLabel("Nothing Playing")
        self.bSizer11.Layout()
        b.paused = True
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

        description = """Recordify is a free program which records music played
on Spotify and saves it for future playback in a MP3 format. 

DO NOT DISTIBUTE COPYWRITTEN MUSIC RECORDED USING RECORDIFY. 
Doing so is illegal.
"""

        licence = """Recordify is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License, 
or (at your option) any later version.

Recordify is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with File Hunter; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA"""

        import wx.adv
        info = wx.adv.AboutDialogInfo()
        ico1_b64 = \
            """
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
"""
# convert back to binary to save it
        ico1 = base64.b64decode(ico1_b64)
        fout = open("recordify.ico", "wb")
        fout.write(ico1)
        fout.close()
        info.SetIcon(wx.Icon('recordify.ico', wx.BITMAP_TYPE_PNG))
        info.SetName('Recordify')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 Chris Puglia')
        info.SetWebSite('http://chrispuglia.com')
        info.SetLicence(licence)
        info.AddDeveloper('Chris Puglia')

        wx.adv.AboutBox(info)

    def __del__(self):
        pass


if __name__ == "__main__":

    b = Backend()
    app = wx.App(False)

    try:
        b.start()
    except OSError:
        dial = wx.MessageDialog(
            None, 'Spotify not detected as open.\nMake sure you have the application running', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        quit()
    icon = wx.Icon()
    icon.CopyFromBitmap(wx.Bitmap("recordify.ico", wx.BITMAP_TYPE_ANY))

    frame = Recordify(parent=None)
    frame.SetIcon(icon)
    frame.Show()

    app.MainLoop()
