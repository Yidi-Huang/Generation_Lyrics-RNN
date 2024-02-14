import os
from collections import defaultdict

# 设置要查找的文件夹路径
folder_path = "hiphop"

# 遍历文件夹内所有文件并统计文件名出现次数
file_counter = defaultdict(list)
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_name = os.path.basename(file_path)
        file_counter[file_name].append(file_path)

# 找出所有名称重复的文件并询问是否删除其中一个
for file_name, file_paths in file_counter.items():
    if len(file_paths) > 1:
        print(f"Found {len(file_paths)} files with the name '{file_name}':")
        for i, file_path in enumerate(file_paths):
            print(f"{i+1}. {file_path}")
        while True:
            choice = input("Do you want to delete one of these files? (y/n)")
            if choice.lower() == "y":
                to_delete = input(
                    "Enter the number of the file you want to delete: ")
                if to_delete.isdigit() and int(to_delete) in range(1, len(file_paths)+1):
                    os.remove(file_paths[int(to_delete)-1])
                    print(f"Deleted file: {file_paths[int(to_delete)-1]}")
                    break
                else:
                    print("Invalid input. Please enter a valid file number.")
            elif choice.lower() == "n":
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
