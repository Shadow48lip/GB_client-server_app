"""
Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными
"""

import json
import pathlib
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    f_name = 'orders.json'

    # проверка существования файла
    path = pathlib.Path(f_name)
    if not path.is_file():
        orders_json = json.loads('{"orders": []}')
    else:
        with open(f_name, encoding='utf-8') as f:
            orders_json = json.load(f)

    # добавление строки заказа
    new_order = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': str(date)}
    orders_json['orders'].append(new_order)

    # запись готового результата в файл (перезапись)
    with open(f_name, 'w', encoding='utf-8') as f:
        json.dump(orders_json, f, indent=4, ensure_ascii=False)

    print('Done')


write_order_to_json('Самокат', 4, 10600.30, 'Alex', datetime.now())
write_order_to_json('Стол', 2, 1505, 'Наталия', datetime.now())
write_order_to_json('Самовар', 100, 6000, 'Виктор Николаевич', datetime.now())
