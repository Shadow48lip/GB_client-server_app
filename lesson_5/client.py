""" Клиент JIM (JSON instant messaging """

import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE
import logging
import logs.client_log_config

LOG = logging.getLogger('app.client')


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

    if __debug__:
        LOG.debug(f'Создан запрос присутствия для клиента {account_name}')

    return msg


def process_ans(message):
    """
    Проверка ответа сервера. Обязательно должен быть код ответа в response.
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            if __debug__:
                LOG.debug(f'Успешный ответ от сервера с кодом {message[RESPONSE]}')
            return '200 : OK'

        LOG.error(f'Ошибочный ответ сервера: код {message[RESPONSE]} - {message[ERROR]}')
        return f'Error code {message[RESPONSE]} : {message[ERROR]}'

    LOG.error(f'Не верный ответ сервера! Нет {RESPONSE} в ответе.')
    raise ValueError


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
        LOG.warning(f'Не указали адрес и порт сервера. Были применены настройки по умолчанию'
              f' {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}')
        server_addr = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
        sys.exit(1)

    # socket
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_addr, server_port))
    msg_out = create_presence('Guest')
    try:
        send_message(s, msg_out)
    except TypeError:
        LOG.critical('Для отправки сообщения нужен словарь с данными.')
        sys.exit(1)

    try:
        msg_in = get_message(s)
        print(process_ans(msg_in))
    except(ValueError, json.JSONDecodeError):
        LOG.eror('Принято некорректное сообщение')
    finally:
        s.close()


if __name__ == '__main__':
    main()
