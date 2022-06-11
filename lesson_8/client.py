""" Клиент JIM (JSON instant messaging """

import json
import sys
import time
import argparse
import threading
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT
from common.decorators import log
import logging
import logs.client_log_config

LOG = logging.getLogger('app.client')


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

    LOG.error(f'Не верный ответ сервера! Не подошел ни один формат ответа. {message}')
    raise ValueError(f'В принятом словаре отсутствуют обязательные поля')


@log
def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""

    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                LOG.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
            else:
                LOG.error(f'Получено некорректное сообщение с сервера: {message}')
        except TypeError:
            # пришло пустое сообщение
            pass
        except ValueError as e:
            LOG.error(f'Не удалось декодировать полученное сообщение. {e}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOG.critical(f'Потеряно соединение с сервером.')
            break


@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""

    help_message = """Поддерживаемые команды:
    message - отправить сообщение. Кому и текст будет запрошены отдельно.
    help - вывести подсказки по командам
    exit - выход из программы
    """

    print(help_message)

    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
            # print(help_message)
        elif command == 'help':
            print(help_message)
        elif command == 'exit':
            create_exit_message(sock, username)
            break
        else:
            print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды.')


# Присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online и регистрации;
@log
def create_presence(sock, account_name='Guest'):
    """
    Создает словарь с сообщением к серверу о присутствии клиента онлайн и отправляет его.
    :param sock:
    :param account_name:
    :return:
    """

    message_dict = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    if __debug__:
        LOG.debug(f'Создан запрос присутствия для клиента {account_name}')

    try:
        send_message(sock, message_dict)
        LOG.info(f'Отправлен запрос присутствия {account_name}')
    except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
        print(e)
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения или команду завершения. Отправляет сформированный словарь"""

    while True:
        to_user = input('Введите получателя сообщения: ')
        if to_user:
            break

    while True:
        message = input('Введите сообщение для отправки: ')
        if message:
            break

    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }

    if __debug__:
        LOG.debug(f'Сформирован словарь сообщения: {message_dict}')

    try:
        send_message(sock, message_dict)
        LOG.info(f'Отправлено сообщение для пользователя {to_user}')
        print('Сообщение отправлено.')
    except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
        print(e)
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def create_exit_message(sock, account_name):
    """Функция создаёт словарь с сообщением о выходе и отпрааляет его"""
    message_dict = {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }

    try:
        send_message(sock, message_dict)
        LOG.info(f'Завершение работы по команде пользователя.')
        # Задержка необходима, чтобы успело уйти сообщение о выходе
        time.sleep(0.5)
        sys.exit(1)
    except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
        print(e)
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)


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
    parser.add_argument('-n', '--name', default='', nargs='?', help='имя пользователя в чате')
    args = parser.parse_args()

    if args.port < 1024 or args.port > 65536:
        LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
        sys.exit(1)

    return args.addr, args.port, args.name


def main():
    # Получаем параметры из командной строки
    server_address, server_port, client_name = arg_parser()

    while True:
        if client_name == '':
            client_name = input('Имя пользователя в чате: ')
        else:
            break

    LOG.info(f'Клиент чата запущен со следующими параметрами:'
             f' {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}, User name: {client_name}')

    # создаем socket
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((server_address, server_port))
    except (ConnectionRefusedError, ConnectionError):
        LOG.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)

    # отправка приветствия и получение ответа
    create_presence(s, client_name)

    try:
        msg_in = get_message(s)
        print(f'Установлено соединение с сервером. Ответ {process_ans(msg_in)}. Пользователь: {client_name}')
    except TypeError as e:
        LOG.critical(e)
        s.close()
        sys.exit(1)
    except(ValueError, json.JSONDecodeError) as e:
        LOG.error(e)
        s.close()
        sys.exit(1)

    # Соединение полностью установлено. Запускаем потоки на чтение и отправку.

    # чтение
    receiver = threading.Thread(target=message_from_server, args=(s, client_name))
    receiver.daemon = True
    receiver.start()

    # отправка с интерактивом
    user_interface = threading.Thread(target=user_interactive, args=(s, client_name))
    user_interface.daemon = True
    user_interface.start()

    if __debug__:
        LOG.debug('Потоки запущены')

    # Watchdog основной цикл, если один из потоков завершён в результате ошибок соединения или выхода пользователя
    # Поскольку все события обрабатываются в зомби в потоках, достаточно просто завершить цикл.
    while True:
        time.sleep(0.5)
        if receiver.is_alive() and user_interface.is_alive():
            continue
        break

    # if client_mode == 'send':
    #     print('Режим отправки сообщений.')
    #     while True:
    #         try:
    #             msg_out = create_message(s)
    #             send_message(s, msg_out)
    #             # получаем код ответа
    #             # print(process_ans(get_message(s)))
    #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
    #             LOG.error(f'Соединение с сервером {server_address} было потеряно.')
    #             sys.exit(1)
    #
    # else:
    #     print('Режим приема сообщений.')
    #     while True:
    #         try:
    #             process_ans(get_message(s))
    #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
    #             LOG.error(f'Соединение с сервером {server_address} было потеряно.')
    #             sys.exit(1)


if __name__ == '__main__':
    main()
