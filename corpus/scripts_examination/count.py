import os

# 遍历文件夹并统计txt文件数量


def count_txt_files(folder_path):
    txt_files_count = 0
    txt_files_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                txt_files_count += 1
                txt_files_names.append(file)
    return txt_files_count, txt_files_names


# 设置文件夹路径和保存文件名的txt文件路径
folder_path = input('Please input the folder path: ')
output_file_path = 'txt_files_names.txt'

# 统计txt文件数量并获取文件名列表
txt_files_count, txt_files_names = count_txt_files(folder_path)

# 将文件名写入txt文件
with open(output_file_path, 'w') as f:
    for file_name in txt_files_names:
        f.write(file_name + '\n')

# 输出结果
print(f'The number of txt files in folder {folder_path} is {txt_files_count}.')
print(f'The file names have been saved to {output_file_path}.')


# 设置文件夹路径
