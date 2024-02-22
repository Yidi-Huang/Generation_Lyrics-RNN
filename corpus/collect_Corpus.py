from lyricsgenius import Genius
import re
import os

token = "DHuxUejky4cCFT0T8hX8s3WzcPL_uC8X3A-PePrGU2JAjq5o2YlwUI8MJEQu79Xg"
genius = Genius(token,timeout=20)



artist_name = "Ariana Grande"

# 创建以艺术家名称命名的目录，确保对艺术家名进行适当的格式化
artist_dir_name = re.sub(r'[\\/*?:"<>|]', "", artist_name)  # 移除Windows系统不允许在文件名中使用的字符
lyrics_dir = os.path.join(os.getcwd(), artist_dir_name)

if not os.path.exists(lyrics_dir):
    os.makedirs(lyrics_dir)

try:
    artist = genius.search_artist(artist_name, max_songs=53, sort='popularity')
    if artist:
        for song in artist.songs:
            # 对歌曲标题进行格式化，移除特殊字符
            song_title_clean = re.sub(r'[\\/*?:"<>|]', "", song.title)
            filepath = os.path.join(lyrics_dir, f"{song_title_clean}.txt")
            
            # 检查歌词是否成功获取
            if song.lyrics:
                # 歌词预处理
                content = song.lyrics.split('\n', 1)[1] if '\n' in song.lyrics else ""  # 删除第一行
                content = re.sub(r'\[.*?\]', '', content)  # 删除所有[]和包含在[]内的内容
                content = re.sub(r'\d+Embed+\b', '', content)  # 删除字符“Embed”和它前面的数字
                content = re.sub(r'\(.*?\)', '', content)  # 删除括号及其内部的内容
                content = re.sub(r'You might also like', '', content)  # 仅删除“You might also like”
                
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"歌词已保存至：{filepath}")
            else:
                print(f"未能获取歌曲 {song.title} 的歌词。")
    else:
        print(f"未找到艺术家：{artist_name}")
except Exception as e:
    print(f"处理过程中发生错误：{e}")