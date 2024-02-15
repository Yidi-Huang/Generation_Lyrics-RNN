from lyricsgenius import Genius
import re

token = "DHuxUejky4cCFT0T8hX8s3WzcPL_uC8X3A-PePrGU2JAjq5o2YlwUI8MJEQu79Xg"
genius = Genius(token)


with open('songs.txt', 'r') as f:
    songlist = []
    for line in f:
        # remove trailing whitespace and split line by '--'
        songname, artist = line.strip().split('--')
        songlist.append(songname)
        song = genius.search_song(songname, artist)
        song.save_lyrics(filename=songname, extension='txt', sanitize=True)

        with open(songname + '.txt', 'r+') as newf:
            content = newf.readlines()
            content = content[1:]
            # 删除所有[]和包含在[]内的内容
            content = [re.sub(r'\[.*?\]', '', line) for line in content]
            # 删除字符“embd”和它前面的数字
            content = [re.sub(r'\d+Embed+\b', '', line) for line in content]
            newf.seek(0)
            newf.writelines(content)
            newf.truncate()
    print("------------------------------------------------------------------------")
    for song in songlist:
        print(song)
