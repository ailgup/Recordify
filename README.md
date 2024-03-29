# Due to changes in the Spotify backend this technique of controlling the player using a localserver no longer works, therefore this codebase must be heavilly modified if one would hope to regain functionality, sorry!

<table><tr><td>
 <img src="https://raw.github.com/ailgup/Recordify/master/images/icon.png"></td><td>
 <h1> Recordify </h1>
 Windows based Spotify MP3 Recorder
 </td></tr></table>
 
## Features
- Record MP3's up to 320kbps
- Automatically grabs song metadata and album art
- Simply drag and drop songs from Spotify to Recordify
- Uses WASAPI interface to record full digital audio (no cords needed!)
- Detects ads and discards them from MP3 (beta)

## Getting Started
### Download Program
[Recordify v1.5](https://github.com/ailgup/Recordify/releases/download/1.5/Recordify.1.5.zip)
### Prerequisites
- Spotify installed and running on PC
- Internet connection

### Recording a song
- Extract the ZIP file and run ```Recordify.exe```
- Drag song(s) from Spotify to Recordify [[gif][drag]]
- Ensure correct playback device and bitrate are selected in Settings [[gif][settings]]
- For optimal results set Spotify volume to 30% [[pic][hundred]]
- Ensure no other applications are making noise
- Choose the desired output directory for the MP3's [[gif][output]]
- Press Play! [[gif][play]]

### While Recording 
- Do not cause other applications to make noise that will mess up the recording
- You can mute output of PC so you don't have to hear every song playing [[gif][mute]]
- Songs will turn yellow while recording and green when recording is complete. [[pic][green]]

## Troubleshooting/Questions

#### Issues with Drag and Drop
- Check if you can drag and drop Spotify songs into a Word document, if so then the issue is Recordify
- We have found that installing python 3.5 x64 and [wxPython Pheonix](https://wxpython.org/Phoenix/snapshot-builds/) should solve your issues

## Legal
In accordance with the [Audio Home Recording Act of 1992](https://en.wikipedia.org/wiki/Audio_Home_Recording_Act)
> "**No action may be brought under this title alleging infringement of copyright** based on the manufacture, importation, or distribution of a digital audio recording device, a digital audio recording medium, an analog recording device, or an analog recording medium, or based **on the noncommercial use by a consumer** of such a device or medium for making digital musical recordings or analog musical recordings."

As with DVR and other media playback services recorded media is intended for the sole purpose of the consumption of the recorder, and may not be distributed in any manner. The creator of this program is in no way responsible for any improper or illegal use of this program, and heavily discourages any such activities. 

## Credits
Thanks to the following projects without which this would not be possible
- pyaudio_portaudio by intxcc
- spotify-local-http-api by Carl Bystrom
- ffmpeg

[green]:https://github.com/ailgup/Recordify/blob/master/images/green.png?raw=true
[play]:https://github.com/ailgup/Recordify/blob/master/images/play.gif?raw=true
[mute]:https://github.com/ailgup/Recordify/blob/master/images/mute.gif?raw=true
[output]:https://github.com/ailgup/Recordify/blob/master/images/output.gif?raw=true
[hundred]:https://github.com/ailgup/Recordify/blob/master/images/hundred.png?raw=true
[settings]:https://github.com/ailgup/Recordify/blob/master/images/settings.gif?raw=true
[drag]:https://github.com/ailgup/Recordify/blob/master/images/drag.gif
