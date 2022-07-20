"""build_constants broken on exe, cannot pull in id and secret
"""


import ssl
from string import ascii_lowercase
from random import choice
import urllib.request
import urllib.parse
import json
import pyaudio
import time
import wave
import threading
from subprocess import call
import os
import base64
try:
    from BUILD_CONSTANTS import *
    print(CLIENT_ID)
except ImportError:
    try:
        with open("creds.txt",'r') as creds:
            CLIENT_ID=creds.readline().split("=")[1].rstrip("\n")
            CLIENT_SECRET=creds.readline().split("=")[1].rstrip("\n")
            print(CLIENT_ID,CLIENT_SECRET)
    except:
        #raise
        print("Unable to get Credentials")
        CLIENT_ID=None
        CLIENT_SECRET=None
class Backend:
    # Default port that Spotify Web Helper binds to.
    PORT = 4381
    DEFAULT_RETURN_ON = ['login', 'logout', 'play', 'pause', 'error', 'ap']
    ORIGIN_HEADER = {'Origin': 'https://open.spotify.com'}
    
    exit_flag = 0
    

    # Use module

    # I had some troubles with the version of Spotify's SSL cert and Python 2.7 on Mac.
    # Did this monkey dirty patch to fix it. Your milage may vary.
    class rec:
        defaultframes = 60
        recorded_frames = []
        p = pyaudio.PyAudio()

        class textcolors:
            blue = '\033[94m'
            green = '\033[92m'
            warning = '\033[93m'
            fail = '\033[91m'
            end = '\033[0m'

        def __init__(self):
            self.currentTrack = None
            self.cwd = os.getcwd()
            print("CWD: ", self.cwd)
            os.makedirs(os.getcwd() + "\\output", exist_ok=True)
            self.saveAs = os.getcwd() + "\\output"
            self.bitrate = "160"

        def recordingPreSetup(self):

            # Set default to first in list or ask Windows
            self.audioList = []
            try:
                default_device_index = self.p.get_default_input_device_info()
            except IOError:
                default_device_index = -1

            # Select Device
            for i in range(0, self.p.get_device_count()):
                info = self.p.get_device_info_by_index(i)
                self.audioList.append(info["name"])
                if default_device_index == -1:
                    default_device_index = info["index"]

            # Handle no devices available
            if default_device_index == -1:
                self.audioList.append("No device available. Restart.")
                print(self.textcolors.fail +
                      "No device available. Quitting." + self.textcolors.end)
            self.device_id = 0  # sets the default as the default

        def recordingSetup(self):
            # Get device info
            try:
                self.device_info = self.p.get_device_info_by_index(
                    self.device_id)
            except IOError:
                self.device_info = self.p.get_device_info_by_index(
                    default_device_index)
                print(self.textcolors.warning +
                      "Selection not available, using default." + self.textcolors.end)

            # Choose between loopback or standard mode
            is_input = self.device_info["maxInputChannels"] > 0
            is_wasapi = (self.p.get_host_api_info_by_index(
                self.device_info["hostApi"])["name"]).find("WASAPI") != -1
            if is_input:
                print(self.textcolors.blue +
                      "Selection is input using standard mode.\n" + self.textcolors.end)
            else:
                if is_wasapi:
                    useloopback = True
                    print(self.textcolors.green +
                          "Selection is output. Using loopback mode.\n" + self.textcolors.end)
                else:
                    print(self.textcolors.fail +
                          "Selection is input and does not support loopback mode. Quitting.\n" + self.textcolors.end)
                    exit()

        def record(self):
            self.recorded_frames = []
            # Open stream
            self.channelcount = self.device_info["maxInputChannels"] if (
                self.device_info["maxOutputChannels"] < self.device_info["maxInputChannels"]) else self.device_info["maxOutputChannels"]
            print(self.textcolors.blue + "Starting..." + self.textcolors.end)
            try:
                self.stream = self.p.open(format=pyaudio.paInt16,
                                          channels=self.channelcount,
                                          rate=int(
                                              self.device_info["defaultSampleRate"]),
                                          input=True,
                                          frames_per_buffer=self.defaultframes,
                                          input_device_index=self.device_info["index"],
                                          as_loopback=True)
            except:
                print("index: ", self.device_info["index"])
                print("id:", self.device_id)
                raise
            self.stream.start_stream()

            # Start Recording
            for i in range(0, int(int(self.device_info["defaultSampleRate"]) / self.defaultframes * self.currentTrack["trackLength"])):
                if self.stream.is_active():
                    self.recorded_frames.append(
                        self.stream.read(self.defaultframes))
                else:
                    print("Inactive Return")
                    return
            print("End Return")

        def stopRecord(self):
            print(self.textcolors.blue + "End." + self.textcolors.end)
            # Stop Recording

            self.stream.stop_stream()

            # Close module
        def save(self):

            filename = self.saveAs + "\\" + \
                self.currentTrack["fileName"] + ".wav"

            waveFile = wave.open(filename, 'wb')
            waveFile.setnchannels(self.channelcount)
            waveFile.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(int(self.device_info["defaultSampleRate"]))
            waveFile.writeframes(b''.join(self.recorded_frames))
            print("Saved as", filename)
            waveFile.close()

            ffmpeg_path = self.cwd + "\\ffmpeg\\bin\\ffmpeg.exe"
            callStr = ("\"" + ffmpeg_path + "\" -loglevel quiet -y -i \"" + self.saveAs + "\\" + self.currentTrack["fileName"] +
                ".wav\" -i temp_album.jpg -map 0:0 -map 1:0 -id3v2_version 3 -write_id3v1 1 -metadata:s:v title=\"Album cover\" "+
                "-metadata:s:v comment=\"Cover (Front)\" -f mp3 -metadata title=\"" + self.currentTrack["trackName"] + "\" -metadata artist=\"" +
                self.currentTrack["artistName"] + "\" -metadata album=\"" + self.currentTrack["albumName"] + "\" -metadata track=\"" +
                self.currentTrack["trackNumber"] + "\" -b:a " + str(self.bitrate) + "K \"" + self.saveAs + "\\" + self.currentTrack["fileName"] + ".mp3\"")
            try:
                print(callStr)
            except UnicodeEncodeError:
                print("still printing crazy names I see")
                pass
            call(callStr, shell=True)
            try:
                os.remove(filename)  # delete temporary file
                os.remove("temp_album.jpg")
            except OSError:
                pass
    @staticmethod
    def _make_authorization_headers():
        auth_header = base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())
        print(auth_header)
        return {'Authorization':'Basic %s' % auth_header.decode()}
    @staticmethod
    def _request_access_token():
        """Gets client credentials access token """
        payload = json.dumps({ 'grant_type': 'client_credentials'}).encode()

        headers = Backend._make_authorization_headers()

        req = urllib.request.Request('https://accounts.spotify.com/api/token', data=payload,
            headers=headers)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read())
        
        if response.status_code is not 200:
            print(response.reason)
        print(response.read())
        token_info = response.json()
        return token_info
    @staticmethod
    def is_token_expired(token_info):
        now = int(time.time())
        return token_info['expires_in'] - now < 60
    @staticmethod
    def new_wrap_socket(*args, **kwargs):
        kwargs['ssl_version'] = ssl.PROTOCOL_SSLv3Test
        return orig_wrap_socket(*args, **kwargs)

    orig_wrap_socket, ssl.wrap_socket = ssl.wrap_socket, new_wrap_socket
    
   
    @staticmethod
    def get_json(url, params={}, headers={}, post=False, token=None):
        if token:
            headers.update({'Authorization':'Bearer '+token['access_token']})
        if post:
            if params:
                params = urllib.parse.urlencode(params).encode('ascii')
            req = urllib.request.Request(url, data=params, headers=headers)
        else:
            if params:
                url += "?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url, headers=headers)
 
        return json.loads(urllib.request.urlopen(req, context=ssl.create_default_context()).read().decode('utf8'))

    @staticmethod
    def generate_local_hostname():
        """Generate a random hostname under the .spotilocal.com domain"""
        #subdomain = ''.join(choice(ascii_lowercase) for x in range(10))
        #return subdomain + '.spotilocal.com'
        return '127.0.0.1'
    @staticmethod
    def get_url(url):
        return "http://%s:%d%s" % (Backend.generate_local_hostname(), Backend.PORT, url)

    @staticmethod
    def get_oauth_token():
        print(Backend.get_json("http://open.spotify.com/token"))
        return Backend.get_json("http://open.spotify.com/token")['t']

    def getAlbumArt(self,id):
        if self.isTokenExpired():
            self.token=Backend.getToken()
        return (((Backend.get_json('https://api.spotify.com/v1/tracks/' + id, token=self.token)).get("album")).get("images")[0]).get("url")
    @staticmethod
    def getToken():
        token=Backend.get_json('https://accounts.spotify.com/api/token',params={ 'grant_type': 'client_credentials'},headers=Backend._make_authorization_headers(), post=True)
        token['expires_at'] = int(time.time()) + token['expires_in']
        return token
    
    def isTokenExpired(self):
        now = int(time.time())
        return self.token['expires_at'] - now < 60

    def getTrackInfo(self, id):
        import re
        if self.isTokenExpired():
            self.token=Backend.getToken()
        k = Backend.get_json('https://api.spotify.com/v1/tracks/' + id, token=self.token)
        trackName = str(k.get('name'))  # keep name as is no need to regex

        fileName = re.sub(r'[/\\:*?"<>|\[\]]', '', trackName)
        artistName = re.sub(r'[\"\']', '', str(
            k.get('artists')[0].get('name')))
        albumName = re.sub(r'[\"\']', '', str(k.get('album').get('name')))
        trackLength = int(k.get('duration_ms')) / 1000
        albumCover = str(((k.get("album")).get("images")[0]).get("url"))
        trackNumber = str(k.get('track_number'))
        status = 'queued'
        currentTrack = {"spotify_id": id, "fileName": fileName, "trackName": trackName, "artistName": artistName,
                        "albumName": albumName, "trackLength": trackLength, "albumCover": albumCover, "trackNumber": trackNumber, "status": status}
        return currentTrack

    @staticmethod
    def get_csrf_token():
        # Requires Origin header to be set to generate the CSRF token.
        print(Backend.get_json(Backend.get_url('/simplecsrf/token.json')))#, headers=Backend.ORIGIN_HEADER))
        return Backend.get_json(Backend.get_url('/simplecsrf/token.json'), headers=Backend.ORIGIN_HEADER)['token']

    def get_status(self, return_after=1, return_on=DEFAULT_RETURN_ON):
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
            'returnafter': return_after,
            'returnon': ','.join(return_on)
        }
        return Backend.get_json(Backend.get_url('/remote/status.json'), params=params, headers=Backend.ORIGIN_HEADER)

    def pause(self, pause=True):
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
            'pause': 'true' if pause else 'false'
        }
        Backend.get_json(Backend.get_url('/remote/pause.json'),
                         params=params, headers=Backend.ORIGIN_HEADER)

    def getVolume(self):
        return self.get_status().get('volume')
    def setVolume(self, volume=100):
        from random import randint
        vol = randint(0, 100) / 100.0
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
            'volume': vol
        }
        print("vol:", vol)
        print(Backend.get_json(Backend.get_url('/remote/volume.json'),
                               params=params, headers=Backend.ORIGIN_HEADER))

    def unpause(self):
        self.pause(pause=False)

    def play(self, spotify_uri):
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
            'uri': "spotify:track:" + spotify_uri,
            'context': spotify_uri,
        }
        Backend.get_json(Backend.get_url('/remote/play.json'),
                         params=params, headers=Backend.ORIGIN_HEADER)

    def open_spotify_client(self):
        return get(Backend.get_url('/remote/open.json'), headers=Backend.ORIGIN_HEADER).text


    def start(self):

        # ghetto hack to work around characters we can't print

        call("set PYTHONIOENCODING=437:replace", shell=True)

        self.total_secs=0
        self.recorded_secs=0
        self.paused = True
        self.num_in_q = -1
        self.list_of_songs = []
        self.song_queue = []
        try:
            self.oauth_token = Backend.get_oauth_token()
            self.csrf_token = Backend.get_csrf_token()
        except:
            raise OSError("Spotify Not Opened")
            return
        #getting the client token
        self.token=Backend.getToken()
        self.r = Backend.rec()
        self.r.recordingPreSetup()

        self.filename = ''  # default value

    def start_playing(self):

        self.num_in_q = 0
        self.r.recordingSetup()
        self.k = {'playing': False}
        while self.num_in_q < len(self.song_queue):
            currentTrack = self.song_queue[self.num_in_q]
            recording = False
            while (not recording):
                self.r.currentTrack = currentTrack
                try:
                    print(str(currentTrack.get("trackName")) + " - " + str(
                        currentTrack.get("artistName")) + "\t" + str(currentTrack.get("albumName")))
                except UnicodeEncodeError:
                    print("Quit printing crazy names")
                    pass
                # start recording
                t = threading.Thread(name=str(currentTrack.get(
                    "trackName")), target=self.r.record, args=())
                t.daemon = True
                try:
                    t.start()
                    self.paused = False
                except (KeyboardInterrupt, SystemExit):
                    cleanup_stop_thread()
                    sys.exit()
                # Play Song
                self.play(currentTrack.get("spotify_id"))
                self.k = {'playing': False}
                while (self.k.get('playing') is False):
                    self.k = self.get_status()
                    if(self.k.get('playing') is False):
                        self.unpause()
                    elif(self.k.get('playing') is True):
                        if not self.k.get('track'):
                            # probs an add
                            self.r.stopRecord()
                            while not self.k.get('track'):
                                self.k = self.get_status()
                                print(self.k)
                                time.sleep(1)
                            break  # this was an add so start over
                        try:
                            time_sleep = int((self.k.get('track')).get(
                                'length')) - int(self.k.get('playing_position'))
                        except:
                            # thinking these could be paused adds, will try and
                            # play?
                            print(self.k)
                            raise
                        print("ZZZ..", time_sleep, "sec")
                        for i in range(time_sleep):
                            if self.paused:
                                print("We be paused")
                                self.r.stopRecord()
                                return
                            else:
                                time.sleep(1)
                    else:
                        pass
                # checking if we paused things, if so we want to stop
                if self.paused:
                    print("We be paused")
                    return
                self.r.stopRecord()
                try:
                    str((self.k.get('track')).get('track_type'))
                except:
                    print("maybe an ad")
                    print(k)
                    pass
                if (str((self.k.get('track')).get('track_type')) == "ad"):
                    print("Bummer it's an ad")
                    self.pause()
                    # waits to give it time to actually stop, makes for a
                    # better recording
                    time.sleep(1)
                    self.paused = True
                    pass
                else:
                    self.r.save()
                    if(os.path.isfile(self.r.saveAs + "\\" + self.r.currentTrack["fileName"] + ".mp3")):
                        self.recorded_secs+=self.song_queue[self.num_in_q]['trackLength']
                        recording = True
                        self.song_queue[self.num_in_q]['status'] = 'complete'
                        self.k = {'playing': False}
                        self.num_in_q += 1
                    else:
                        print("Could not find ", self.r.saveAs + "\\" +
                              self.r.currentTrack["fileName"] + ".mp3")
                        self.song_queue[self.num_in_q]['status'] = 'retry'
                        self.pause()
                        # waits to give it time to actually stop, makes for a
                        # better recording
                        time.sleep(1)
                        self.paused = True
        self.paused = True
        print("Completed all songs")
