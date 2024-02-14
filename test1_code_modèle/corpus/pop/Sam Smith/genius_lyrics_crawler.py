from lyricsgenius import Genius
import os
import requests
from bs4 import BeautifulSoup
import re


# ！！！控制使用频率，否则容易被限制访问！！！

def download_lyrics(artist_name):
    # 创建一个文件夹用于保存歌词文件
    if not os.path.exists(artist_name):
        os.makedirs(artist_name)

    # 通过网络获得该歌手在Billboard上前10首热门歌曲的URL
    url = f'https://www.billboard.com/music/{artist_name}/chart-history'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.find_all("h3", {"class": "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only artist-chart-row-title"})

    # 遍历所有歌曲并下载歌词
    for i in range(min(len(songs), 10)):
        song_name = songs[i].text.strip()
        song_name = re.sub(r'[^\w\s]', '', song_name)
        artist = re.sub(r'[^\w\s]', '', artist_name)
        with open(f"songs.txt", "a", encoding="utf-8") as f:
            f.write(song_name + "--" + artist + "\n")


if __name__ == '__main__':
    artist_name = input("请输入歌手名字：")
    if " " in artist_name:
        artist_name = artist_name.replace(" ", "-")
        download_lyrics(artist_name.lower())
    else:
        download_lyrics(artist_name.lower())


# download_lyrics through Genius API
token = "DHuxUejky4cCFT0T8hX8s3WzcPL_uC8X3A-PePrGU2JAjq5o2YlwUI8MJEQu79Xg"
genius = Genius(token)


with open('songs.txt', 'r') as f:
    for line in f:
        # remove trailing whitespace and split line by '--'
        songname, artist = line.strip().split('--')
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
