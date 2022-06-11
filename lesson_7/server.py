""" Сервер JIM (JSON instant messaging """
# текущая версия сервера принимает сообщения от одних клиентов и тут же рассылает их всем, кто читает

import argparse
import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import json
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE, CONNECTION_TIMEOUT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from common.decorators import log
import logging
import logs.server_log_config

LOG = logging.getLogger('app.server')


@log
def process_client_message(message, messages_list, sock):
    """
    Обрабатывает сообщения от клиентов на соответствие протоколу JIM и возвращает словарь с ответом.
    :param messages_list:
    :param message:
    :return answer dict:
    """

    if ACTION not in message or TIME not in message:
        if __debug__:
            LOG.warning(f'Пришли неизвестные данные - {message}. Ответ - Bad request')
        return {RESPONSE: 400, ERROR: 'Bad request'}

    # Код по молчанию
    return_code = 200

    # Присутствие клиента online;
    if message[ACTION] == PRESENCE:
        if message[USER][ACCOUNT_NAME] == 'Guest':
            if __debug__:
                LOG.debug(f'Ответ клиенту на {message[ACTION]}. Код {return_code}')
            send_message(sock, {RESPONSE: return_code})
            return True
        else:
            return_code = 401
            if __debug__:
                LOG.debug(f'Ответ клиенту. Код {return_code}')
            send_message(sock, {RESPONSE: return_code, ERROR: f'Not authorize account {message[USER][ACCOUNT_NAME]}'})
            return True

    # получили сообщение от клиента и сообщили ему об удачном приему
    elif message[ACTION] == MESSAGE and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))

        if __debug__:
            LOG.debug(f'Ответ клиенту на {message[ACTION]}. Код {return_code}')
        send_message(sock, {RESPONSE: return_code})
        return True


    # для неизвестных экшенов
    return_code = 400
    LOG.info(f'Ответ клиенту на {PRESENCE}. Код {return_code}. Неизвестный {ACTION}')
    send_message(sock, {RESPONSE: return_code, ERROR: f'Action {message[ACTION]} not support'})
    return True


@log
def read_requests(read_clients, all_clients):
    """Чтение запросов из списка клиентов"""

    requests = {}

    for sock in read_clients:
        try:
            msg_in = get_message(sock)
            # print('msg_in', msg_in)
            requests[sock] = msg_in
        except json.JSONDecodeError as e:
            LOG.warning(f'Ошибка парсинга JSON: {e}')
        except ValueError as e:
            # print('value error', e, sock.fileno(), sock.getpeername())
            LOG.warning(f'Принято некорректное сообщение или Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            all_clients.remove(sock)
        except ConnectionResetError as e:
            LOG.warning(f'Клиент закрыл соединение! Сокет отключен')
            sock.close()
            all_clients.remove(sock)

    return requests


@log
def write_responses(requests, clients_write, all_clients):
    """Ответ сервера клиентам, от которых были запросы"""

    for sock in clients_write:
        if sock in requests:
            try:
                if requests[sock] == '':
                    raise ValueError
                msg_in = requests[sock]
                msg_out = process_client_message(msg_in, [])
                send_message(sock, msg_out)
            except TypeError:
                LOG.error(f'Для отправки сообщения нужен словарь с данными. Не отправилось: {msg_out}')
            except Exception as e:
                all_clients.remove(sock)
                sock.close()


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

            # имеет смысл проверять select, если есть клиенты в пуле
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
                        process_client_message(get_message(client_with_message), messages, client_with_message)
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
            if clients_write and messages:
                for _ in range(len(messages)):
                    msg = messages.pop()

                    message = {
                        ACTION: MESSAGE,
                        SENDER: msg[0],
                        TIME: time.time(),
                        MESSAGE_TEXT: msg[1]
                    }

                    for waiting_client in clients_write:
                        try:
                            print('отправили сообщение', waiting_client, message)
                            send_message(waiting_client, message)
                        except:
                            # LOG.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                            LOG.info(f'Клиент  отключился от сервера.')
                            waiting_client.close()
                            all_clients.remove(waiting_client)

                # # читает из sock.recv и возвращает словарь с входящими сообщениями в json
                # requests = read_requests(clients_read, all_clients)
                # print('requests:', requests)
                # if requests:
                #     for request in requests:
                #         # на каждое сообщение отвечаем кодом, а если это послание, то складываем в список
                #         msg_out = process_client_message(request, messages)
                #         if request in clients_write:
                #             send_message(request, msg_out)
                #
                #
                #     write_responses(requests, clients_write, all_clients)


if __name__ == '__main__':
    main()
