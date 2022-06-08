import json

def participle(filename):
    data = json.loads(open(f"/data/{filename}", "r"))




    data_part = {}
    json.dump(data_part, f"json文件/part_{filename}", "w")