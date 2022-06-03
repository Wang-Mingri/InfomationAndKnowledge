


def getDataFilename(index, pieces):
    temp_list = []
    for piece in pieces:
        filename_list = []
        if piece not in index:
            temp_list.append(filename_list)
        else:
            filename_list = [int(key) for key in index[piece].keys()] # 查找对应文档对应的编号id
            filename_list.sort() # 对文档编号排序
            temp_list.append(filename_list)
    list = []
    for i in temp_list:
        list += i
    return sorted(set(list))
