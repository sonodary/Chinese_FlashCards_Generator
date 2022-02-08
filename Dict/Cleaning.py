import json

with open('Chinese_dict.json') as json_data:
    data = json.load(json_data)
    for key, value in data.items():
        if "traditional" in value:
            del value["traditional"]
        if "simplified" in value:
            del value["simplified"]


with open("Reduced_dict.json", "w") as outfile:
    json.dump(data, outfile, ensure_ascii=False)