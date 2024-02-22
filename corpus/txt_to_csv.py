import csv
import os

# 替换为你的歌词文件夹路径
lyrics_folder_path = 'Ariana Grande'
# 歌手名，假设是文件夹的名字
artist_name = os.path.basename(lyrics_folder_path)
# CSV文件的完整路径
csv_file_path = os.path.join(lyrics_folder_path, f"{artist_name}.csv")

# 准备CSV文件，写入标题行
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Artist', 'Title', 'Lyrics'])

    # 遍历文件夹中的所有文件
    for filename in os.listdir(lyrics_folder_path):
        if filename.endswith('.txt'):
            # 文件名的格式是 "歌曲标题.txt"
            title = filename.replace('.txt', '')
            # 读取歌词内容
            with open(os.path.join(lyrics_folder_path, filename), 'r', encoding='utf-8') as file:
                lyrics = file.read()
            # 写入CSV
            csvwriter.writerow([artist_name, title, lyrics])

print(f"CSV文件已生成：{csv_file_path}")
