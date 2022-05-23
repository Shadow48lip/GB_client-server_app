""" Клиент JIM (JSON instant messaging """

import sys, json, socket, time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE
from common.utils import get_message, send_message


# Присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online;
def create_presence(account_name='Guest'):
    """
    Создает словарь с сообщением к серверу о присутствии клиента онлайн.
    :param account_name:
    :return:
    """

    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return msg


def process_ans(message):
    """
    Проверка ответа сервера. Обязательно должен быть код ответа в response.
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return 'Return code: 200. OK'
        return f'Error code: {message[RESPONSE]}. {message[ERROR]}'
    return ValueError


def main():
    """
    Разбор параметров командной строки.
    client.py 127.0.0.1 8888
    """
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65536:
            raise ValueError
    except IndexError:
        print(f'Не указали адрес и порт сервера. Были применены настройки по умолчанию'
              f' {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}')
        server_addr = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Номер порта должен быть указан в пределах 1024 - 65635')
        sys.exit(1)

    # socket
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_addr, server_port))
    msg_out = create_presence('Guest')
    try:
        send_message(s, msg_out)
    except TypeError:
        print('Для отправки сообщения нужен словарь с данными.')

    try:
        msg_in = get_message(s)
        print(process_ans(msg_in))
    except(ValueError, json.JSONDecodeError):
        print('Принято некорректное сообщение')


if __name__ == '__main__':
    main()
