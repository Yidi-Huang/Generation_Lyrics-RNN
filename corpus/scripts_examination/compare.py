# 定义比较函数
def compare_files(file1_path, file2_path):
    # 读取文件内容并转换为集合
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        file1_contents = set(f1.read().splitlines())
        file2_contents = set(f2.read().splitlines())
    # 使用集合操作计算差异
    unique_to_file1 = file1_contents - file2_contents
    # 输出结果
    for song in unique_to_file1:
        print(song)


# 设置要比较的文件路径
file2_path = 'files.txt'
file1_path = 'ecel.txt'
# 进行比较并输出结果
compare_files(file1_path, file2_path)
