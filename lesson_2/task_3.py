"""
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
"""

import yaml

source_dict = {
    '1$': [1, 2, 3, 4, 5],
    '2¥': 1000,
    '3₽': {'name': 'Иван', 'age': 33},
}


with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(source_dict, f, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f:
    dict_from_yaml = yaml.load(f, Loader=yaml.FullLoader)

print('исходный словарь', type(source_dict))
print(source_dict)
print('считанный из yaml файла словарь', type(dict_from_yaml))
print(dict_from_yaml)
print('идентичны ли словари:', source_dict == dict_from_yaml)