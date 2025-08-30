#!/usr/bin/env python3

from utils import get_files_with_ext, filter_with_ext
from musicClasses import Song, Album
import os


#path = r'D:\gitRepos\tiago\audity\resources\songs'
path = "/home/tiago/GitRepos/tiago/audity/resources/songs"
#path2 = "C:/Users/tiago/Music"
path2 = "/home/tiago/Music"
extensions = ['mp3', 'wav', 'm4a', 'flac']
# aac, aiff, alac, , ogg, raw
# PCM depth, sample rate




def getSongs():
    fileList = get_files_with_ext(path, extensions)
    fileList2 = get_files_with_ext(path2, extensions)
    fileList = fileList + fileList2

    return fileList


def getAlbums():
    iter = os.walk(path)
#    iter2 = os.walk(path2)

    # for root, dirs, files in iter:
    # print(dirs)
    # break

    next(iter)
    
    albums = []
    for root, dirs, files in iter:
        # print(root)# for album in albums:
        if os.path.samefile(os.path.dirname(root), path):
            # print(root)
            albums.append(Album(os.path.basename(root), filter_with_ext(files, extensions)))

#    next(iter2)
    
#    for root, dirs, files in iter2:
#        # print(root)# for album in albums:
#        if os.path.samefile(os.path.dirname(root), path2):
#            print(root)
#            albums.append(Album(os.path.basename(root), filter_with_ext(files, extensions)))

#    for album in albums:
#        print(album)
#        print("")

    return albums

if __name__=="__main__":
        getAlbums()
