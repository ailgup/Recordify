# -*- coding: utf-8 -*-

# A simple setup script to create an executable running wxPython. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# wxapp.py is a very simple 'Hello, world' type wxPython application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
import requests
import base64
import os
from cx_Freeze import setup, Executable
import urllib.request
# n.b. vaerioning must be #.# where I is an integer of any length
try:
    with open("creds.txt",'r') as creds:
        CLIENT_ID=creds.readline().split("=")[1].rstrip("\n")
        CLIENT_SECRET=creds.readline().split("=")[1].rstrip("\n")
        print("ID:",CLIENT_ID," SEC:",CLIENT_SECRET)
except:
    raise
def getVersion():
    latest_url='https://github.com/ailgup/Recordify/releases/latest'
    result=urllib.request.urlopen(latest_url)
    return float(result.geturl().split("/")[-1])

def nextVersion(increment_major=False):
    current=str(getVersion()).split(".")
    if increment_major:
        return str(int(current[0])+1)+".0"
    else:
        return current[0]+"."+str(int(current[1])+1)


VERSION=nextVersion()
#VERSION_STR="VERSION=%s" % VERSION
#print("V:",VERSION_STR)  
include_files = ['ffmpeg\\', (requests.certs.where(), 'cacert.pem'), 'addRemover.exe',
                 'add.png', 'check.png', 'speaker.png', 'folder.bmp', 'play.bmp', 'pause.bmp', 'rec_50px.png']
build_exe_options = {"include_msvcr": True, 
                    "packages": ["os", "wx", "urllib.request", "urllib.parse", "ssl"], 
                    'include_files': include_files,
                    'build_exe':'build\Recordify '+VERSION,
                    'constants' : 'VERSION=\"'+VERSION+'\",CLIENT_ID=\"'+CLIENT_ID+'\",CLIENT_SECRET=\"'+CLIENT_SECRET+"\""
                    }
print('VERSION=\"'+VERSION+'\",CLIENT_ID=\"'+CLIENT_ID+'\",CLIENT_SECRET=\"'+CLIENT_SECRET+"\"")

if sys.platform == 'win32':
    base = 'Win32GUI'
#base = None
executables = [
    Executable(
        'gui3.py',
        base=base,
        icon="recordify.ico",
        targetName="Recordify.exe"
    )
]

setup(name='Recordify',
      version=VERSION,
      requires=["requests"],
      description='Spotify Recorder',
      options={"build_exe": build_exe_options},
      executables=executables
      )
