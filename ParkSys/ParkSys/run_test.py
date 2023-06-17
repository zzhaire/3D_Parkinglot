def read_map(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        park_map = []
        for line in lines:
            row = line.strip().split()
            park_map.append(row)
    return park_map 

file_name = '../data/map.dat'
matrix = read_map(file_name)

# 打印输出二维数组
for row in matrix:
    print(row)

