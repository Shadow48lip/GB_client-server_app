"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV
"""

import pathlib
import chardet
import re
import csv


def get_data(f_names):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for f_name in f_names:
        # проверка существования файла
        path = pathlib.Path(f_name)
        if not path.is_file():
            print(f'file {f_name} not exist')
            continue

        # поиск кодировки файла и раскодировка
        with open(f_name, 'rb') as fb:
            data_bytes = fb.read()
            charset = chardet.detect(data_bytes)['encoding']
            # print('file codetable:', charset)

            data_str = data_bytes.decode(encoding=charset)
            # print(data_str)
            result = re.search(r'Изготовитель ОС:\s+([\w\s]+)\r\n', data_str)
            os_prod_list.append(result[1])
            # print(result[1])

            result = re.search(r'Название ОС:\s+([\w\.\s]+)\r\n', data_str)
            os_name_list.append(result[1])
            # print(result[1])

            result = re.search(r'Код продукта:\s+([\w\-\s]+)\r\n', data_str)
            os_code_list.append(result[1])
            # print(result[1])

            result = re.search(r'Тип системы:\s+([\w\-\s]+)\r\n', data_str)
            os_type_list.append(result[1])
            # print(result[1])

    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data


def write_to_csv(csv_f_name, data_f_name):
    data = get_data(data_f_name)
    with open(csv_f_name, 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        f_n_writer.writerows(data)


data_filenames = ['info_1.txt', 'info_2.txt', 'info_3.txt']

write_to_csv('task_1.csv', data_filenames)

print('Done')
