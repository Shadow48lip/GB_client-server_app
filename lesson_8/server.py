""" Сервер JIM (JSON instant messaging """
# текущая версия сервера принимает сообщения от одних клиентов и тут же рассылает их всем, кто читает

import argparse
import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE, CONNECTION_TIMEOUT, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT
from common.utils import get_message, send_message
from common.decorators import log
import logging
import logs.server_log_config

LOG = logging.getLogger('app.server')


@log
def process_client_message(message, messages_list, sock, all_clients, names):
    """
    Обрабатывает принятые сообщения от клиентов на соответствие протоколу JIM и возвращает словарь с ответом.
    :param message: словарь с новым сообщением
    :param messages_list: массив с сообщениями клиентов
    :param sock: сокет  с новым сообщением
    :param all_clients: все подключенные клиенты
    :param names: словарь с зарегистрированными клиентами
    :return:
    """

    if __debug__:
        LOG.debug(f'Разбор входящего сообщения: {message}')

    if ACTION not in message or TIME not in message:
        if __debug__:
            LOG.warning(f'Пришли неизвестные данные - {message}. Ответ - Bad request')
        return {RESPONSE: 400, ERROR: 'Bad request'}

    # Код по молчанию
    return_code = 200

    # Присутствие клиента online;
    # регистрация пользователя, если он новый
    if message[ACTION] == PRESENCE and ACCOUNT_NAME in message[USER]:
        new_user = message[USER][ACCOUNT_NAME]

        if new_user not in names.keys():
            if __debug__:
                LOG.debug(f'Зарегистрировали нового пользователя {new_user}')
            names[new_user] = sock
            send_message(sock, {RESPONSE: return_code})
            return True
        else:
            return_code = 400
            if __debug__:
                LOG.debug(f'Пользователь уже добавлен. Код {return_code}')
            send_message(sock, {RESPONSE: return_code, ERROR: f'Пользователь {new_user} уже зарегистрирован.'})
            return True

    # получили сообщение от клиента и сообщили ему об удачном приеме
    elif message[ACTION] == MESSAGE and MESSAGE_TEXT in message and DESTINATION in message and SENDER in message:
        messages_list.append(message)

        # if __debug__:
        #     LOG.debug(f'Ответ клиенту на {message[ACTION]}. Код {return_code}')
        # send_message(sock, {RESPONSE: return_code})
        return True

    # клиент отключается
    elif message[ACTION] == EXIT and ACCOUNT_NAME in message:
        all_clients.remove(names[message[ACCOUNT_NAME]])
        del names[message[ACCOUNT_NAME]]
        LOG.info(f'Пользователь {message[ACCOUNT_NAME]} прислал команду выхода')
        sock.close()
        return

    # для неизвестных экшенов
    return_code = 400
    LOG.info(f'Ответ клиенту на {PRESENCE}. Код {return_code}. Неизвестный {ACTION}')
    send_message(sock, {RESPONSE: return_code, ERROR: f'Action {message[ACTION]} not support'})
    return True


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированных пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """

    if message[DESTINATION] not in names:
        message_dict = {
            ACTION: MESSAGE,
            SENDER: 'Server',
            DESTINATION: message[SENDER],
            TIME: time.time(),
            MESSAGE_TEXT: f'Пользователь {message[DESTINATION]} не зарегистрирован.'
        }
        send_message(names[message[SENDER]], message_dict)
        LOG.error(f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, отправка сообщения невозможна.')
        return

    if names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError

    send_message(names[message[DESTINATION]], message)
    LOG.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}.')

    return


@log
def arg_parser():
    """
    Разбор параметров командной строки.
    server.py -p 8888 -a 127.0.0.1
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='', nargs='?',
                        help=f'Server address. Default - all net interfaces')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?',
                        help=f'Server port 1024-65535. Default {DEFAULT_PORT}')
    args = parser.parse_args()

    if not 1023 < args.p < 65536:
        LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
        sys.exit(1)

    return args.a, args.p


def main():
    # Получаем параметры из командной строки
    listen_address, listen_port = arg_parser()

    # сокеты клиентов
    all_clients = []
    # очередь сообщений для рассылки
    messages = []
    # словарь с зарегистрированными пользователями и их сокетам
    names = {}

    # listen server socket
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Несколько приложений может слушать сокет
        s.bind((listen_address, listen_port))
        s.listen(MAX_CONNECTIONS)
        s.settimeout(CONNECTION_TIMEOUT)
        print(f'Server ready. Listen connect on {listen_address}:{listen_port}')
        LOG.info(f'Server start. Listen connect on {listen_address}:{listen_port}')

        # listen clients connections
        while True:
            try:
                client_socket, client_address = s.accept()
            except OSError as err:  # timeout
                # print(err.errno)
                pass
            else:
                LOG.info(f'Получен запрос на соединение от {str(client_address)}')
                print(f"Получен запрос на соединение от {str(client_address)}")
                all_clients.append(client_socket)

            wait = 0.1
            clients_read = []
            clients_write = []

            # имеет смысл проверять select, если есть клиенты в пуле дабы сервер не зависал на ожидании (асинхронность)
            if all_clients:
                try:
                    clients_read, clients_write, errors = select(all_clients, all_clients, [], wait)
                except OSError:
                    pass
                except Exception as e:
                    print('ошибка в select:', e)

            # обработка входящих сообщений
            if clients_read:
                for client_with_message in clients_read:
                    try:
                        print(f'пришло сообщение от {client_with_message.getpeername()}')
                        process_client_message(get_message(client_with_message), messages, client_with_message,
                                               all_clients, names)
                    except OSError:
                        print('Отправитель отключился')
                        LOG.info(f'Отправитель отключился от сервера.')
                        all_clients.remove(client_with_message)
                        client_with_message.close()
                    except Exception as e:
                        print('Отправитель отключился', client_with_message.getpeername())
                        LOG.info(f'Отправитель {client_with_message.getpeername()} отключился от сервера.')
                        all_clients.remove(client_with_message)
                        client_with_message.close()

            # обработка слушающих клиентов
            if messages:
                for _ in range(len(messages)):
                    msg = messages.pop()

                    try:
                        process_message(msg, names, clients_write)
                    except Exception:
                        LOG.info(f'Связь с клиентом с именем {msg[DESTINATION]} была потеряна')
                        all_clients.remove(names[msg[DESTINATION]])
                        names[msg[DESTINATION]].close()
                        del names[msg[DESTINATION]]


if __name__ == '__main__':
    main()
