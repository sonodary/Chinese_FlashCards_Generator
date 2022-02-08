import pinyin as py
import json

# Create a json dictionary from original dictionary
with open('cedict_ts.u8') as file:
    Chinese_text = file.read()
    lines = Chinese_text.split('\n')
    dict_lines = list(lines)

    def parse_line(line):
        parsed = {}
        if line == '':
            dict_lines.remove(line)
            return 0
        line = line.rstrip('/').split('/')
        if len(line) <= 1:
            return 0
        translated_english = line[1:]
        characters = line[0].split('[')[0].split()
        traditional = characters[0]
        simplified = characters[1]
        pinyin = py.get(simplified)
        parsed['traditional'] = traditional
        parsed['simplified'] = simplified
        parsed['pinyin'] = pinyin
        parsed['english'] = translated_english
        list_of_dicts.append(parsed)


    def main():
        # make each line into a dictionary
        for line in dict_lines:
            parse_line(line)

        return list_of_dicts


list_of_dicts = []
parsed_dict = main()

Chinese_dict = {}
for word in parsed_dict:
    simplified = word["simplified"]
    Chinese_dict[simplified] = word

with open("Chinese_dict.json", "w") as file:
    json_dict = json.dump(Chinese_dict, file, ensure_ascii=False)


