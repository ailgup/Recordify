import os
import ctypes
import sys


def writeFile():
    urls = ['pubads.g.doubleclick.net', 'securepubads.g.doubleclick.net',
            'www.googletagservices.com', 'gads.pubmatic.com', 'ads.pubmatic.com', 'spclient.wg.spotify.com']
    str = "\n"
    for u in urls:
        str += '0.0.0.0 ' + u + "\n"

    try:
        path = os.environ.get('windir') + "\\System32\\drivers\\etc\\hosts"

        if str in open(path).read():
            return
        else:
            with open(path, "a") as myfile:
                myfile.write(str)
            return
    except PermissionError:
        return
    except:
        raise


writeFile()
