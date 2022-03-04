import os



dir_path = '../prepared/san'
files=os.listdir(dir_path)
result_file = 'data.txt'

# for file in files:
#     print(file)
#     file_path = os.path.join(dir_path, file)  # 连接路径
#     with open(file_path, 'r', encoding='utf-8') as f_raw:
#         data = [line.split('*')[0].strip() for line in f_raw.readlines()]
#     with open(result_file, 'a+', encoding='utf-8') as f_new:
#         f_new.write(str(data) + '\n')

with open(result_file, 'r', encoding='utf-8') as f_new:
    data = [eval(line.strip())for line in f_new.readlines()]
    # print(data)
    # print(type(data))
    for row in data:
        print(row)
        print(type(row))


