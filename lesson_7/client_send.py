""" Клиент JIM (JSON instant messaging """
""" только отправка сообщений """

import json
import sys
import time
import argparse
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE, MESSAGE, MESSAGE_TEXT, SENDER
from common.decorators import log
import logging
import logs.client_log_config

LOG = logging.getLogger('app.client')


# Присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online;
@log
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


@log
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
    elif ACTION in message:
        if message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
            print(f'Получено сообщение от пользователя '
                  f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            LOG.info(f'Получено сообщение от пользователя '
                        f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            return True

    LOG.error(f'Не верный ответ сервера! Не подошел ни один формат ответа. {message}')
    raise ValueError(f'В принятом словаре отсутствуют обязательные поля')


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения или команду завершения. Возвращает ловарь в формате JIM"""

    message = input('Введите сообщение для отправки или "!!!" для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOG.info('Завершение работы по команде пользователя.')
        print('До свидания')
        time.sleep(2)
        sys.exit(0)

    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }

    if __debug__:
        LOG.debug(f'Сформирован словарь сообщения: {message_dict}')

    return message_dict


@log
def arg_parser():
    """
    Разбор параметров командной строки.
    client.py 127.0.0.1 8888 -m send
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?',
                        help=f'Server address. Default {DEFAULT_IP_ADDRESS}')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?',
                        help=f'Server port 1024-65535. Default {DEFAULT_PORT}')
    parser.add_argument('-m', '--mode', default='send', nargs='?', help='send or listen mode')
    args = parser.parse_args()

    if args.port < 1024 or args.port > 65536:
        LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
        sys.exit(1)

    return args.addr, args.port, args.mode


def main():
    # Получаем параметры из командной строки
    server_address, server_port, client_mode = arg_parser()

    if client_mode != 'send' and client_mode != 'listen':
        LOG.warning('Указанный режим работы не поддерживается! Укажите send или listen')
        sys.exit(1)

    LOG.info(f'Клиент запущен со следующими параметрами:'
             f' {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}, Mode: {client_mode}')

    # создаем socket
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((server_address, server_port))
    except ConnectionRefusedError:
        LOG.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)

    # отправка приветствия и получение ответа
    try:
        msg_out = create_presence('Guest')
        send_message(s, msg_out)

        msg_in = get_message(s)
        print(process_ans(msg_in))
    except TypeError as e:
        LOG.critical(e)
        s.close()
        sys.exit(1)
    except(ValueError, json.JSONDecodeError) as e:
        LOG.error(e)
        s.close()
        sys.exit(1)

    if client_mode == 'send':
        print('Режим отправки сообщений.')
        while True:
            try:
                msg_out = create_message(s)
                send_message(s, msg_out)
                # получаем код ответа
                # print(process_ans(get_message(s)))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                LOG.error(f'Соединение с сервером {server_address} было потеряно.')
                sys.exit(1)

    else:
        print('Режим приема сообщений.')
        while True:
            try:
                process_ans(get_message(s))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                LOG.error(f'Соединение с сервером {server_address} было потеряно.')
                sys.exit(1)


if __name__ == '__main__':
    main()
