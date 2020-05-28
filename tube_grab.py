from __future__ import unicode_literals
from bs4 import BeautifulSoup as bs
import requests
import youtube_dl
import sys
import re
import os




def usage():
    print("{} [song list file]".format(sys.argv[0]))
    sys.exit(0)


class MyLogger(object):
    def debug(self, msg):
        #print(msg)
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...\n')

def main():
    search_base = "https://www.youtube.com/results?search_query={}"
    watch_base = "https://www.youtube.com{}"
    ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist' : True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
    print("Loaded configs..")
    fname = sys.argv[1]
    #link_list = []
    song_link = {}
    with open(fname, "r", encoding="utf-8") as f:
        for song in f.readlines():
            song = song.strip("\n")
            print("Searching for {}...\t".format(song), end='')
            r = requests.get(search_base.format(song))
            bso = bs(r.content, "html.parser")
            parse(bso, song, song_link)
        
    if not os.path.isdir("Songs"):
        os.mkdir("Songs")
    os.chdir("Songs")
    print("In Songs dir...")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("#"*40)
        for song in song_link:
            link = watch_base.format(song_link[song])
            print("Grabbing [ {} ] from [ {} ] to download....".format(song, link))
            ydl.download([link])
    print("#"*60)

def parse(bso, song, song_link):
    #print("Parsing return data...")
    #print("{}\n".format(bso))
    rr = re.compile('\\n\\n((\\d)?\\d):(\\d\\d)')
    #rs = re.compile("^{}.*".format(song))
    al = []
    for a in bso('a'):
        al.append(a)
    for i, l in enumerate(al):
        if re.search(rr, l.text):
            title = al[i+1].text
            uri = al[i+1]['href']
            song_link.update({ title : uri })
            print("\t[+] Got back {}".format(title))
            return

if __name__=="__main__":
    main()
		
