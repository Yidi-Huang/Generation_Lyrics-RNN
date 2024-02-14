# 定义文本文件路径
file1_path = 'files.txt'
file2_path = 'ecel.txt'

# 打开文件并读取每一行字符串
with open(file1_path, "r") as f:
    lines1 = f.readlines()


with open(file2_path, "r") as f:
    lines2 = f.readlines()

# 去除每行字符串末尾的换行符
lines1 = [line.strip() for line in lines1]
lines2 = [line.strip() for line in lines2]

print(len(lines1))
print(len(lines2))
for line in lines1:
    if line not in lines2:
        print(line)
    else:
        print('文件相同')
