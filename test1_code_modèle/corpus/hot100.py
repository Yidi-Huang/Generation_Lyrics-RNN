import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.billboard.com/charts/year-end/2018/hot-country-songs/'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.find_all("li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 lrv-u-border-color-grey-light lrv-u-padding-l-2 lrv-u-padding-l-1@mobile-max")
    with open('hottest_country_songs2018.txt', 'w') as f:
        for song in songs:
            # 提取歌曲名称和演唱者
            song_name = song.find('h3', class_='c-title').text.strip()
            artist_name = song.find('span', class_='c-label').text.strip()
            # 格式化输出到文件中
            formatted_song = re.sub(
                r'[^\w\s]', '', song_name) + '--' + re.sub(r'[^\w\s]', '', artist_name)
            f.write(f'{formatted_song}\n')
    print('Done! Top country songs saved to hottest_country_songs2005.txt')
else:
    print('Error getting data from website.')
