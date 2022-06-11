""" Сервер JIM (JSON instant messaging """
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import json
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE
from common.utils import get_message, send_message
from common.decorators import log
import logging
import logs.server_log_config

LOG = logging.getLogger('app.server')


@log
def process_client_message(message):
    """
    Обрабатывает сообщения от клиентов на соответствие протоколу JIM и возвращает словарь с ответом.
    :param message:
    :return answer dict:
    """

    if ACTION not in message or TIME not in message:
        if __debug__:
            LOG.warning(f'Пришли неизвестные данные - {message}. Ответ - Bad request')
        return {RESPONSE: 400, ERROR: 'Bad request'}

    # Присутствие клиента online;
    if message[ACTION] == PRESENCE:
        if message[USER][ACCOUNT_NAME] == 'Guest':
            return_code = 200
            if __debug__:
                LOG.debug(f'Ответ клиенту на {PRESENCE}. Код {return_code}')
            return {RESPONSE: return_code}
        else:
            return_code = 401
            if __debug__:
                LOG.debug(f'Ответ клиенту. Код {return_code}')
            return {RESPONSE: return_code, ERROR: f'Not authorize account {message[USER][ACCOUNT_NAME]}'}
    else:
        # для неизвестных экшенов
        return_code = 400
        LOG.info(f'Ответ клиенту на {PRESENCE}. Код {return_code}. Неизвестный {ACTION}')
        return {RESPONSE: return_code, ERROR: f'Action {message[ACTION]} not support'}


def main():
    """
    Разбор параметров командной строки.
    server.py -p 8888 -a 127.0.0.1
    """

    # tcp port
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65536:
            raise ValueError
    except IndexError:
        LOG.critical(f'После параметра -p необходимо указать номер порта. По умолчанию будет выставлен {DEFAULT_PORT}')
        sys.exit(1)
    except ValueError:
        LOG.critical('Номер порта должен быть указан в пределах 1024 - 65635')
        sys.exit(1)

    # tcp address
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        LOG.critical(f'После параметра -a необходимо указать слушающий ip адрес. По умолчанию - все доступные адреса.')
        sys.exit(1)

    # listen server socket
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Несколько приложений может слушать сокет
    s.bind((listen_address, listen_port))
    s.listen(MAX_CONNECTIONS)
    print(f'Server ready. Listen connect on {listen_address}:{listen_port}')
    LOG.info('Server start')

    # listen clients connections
    try:
        while True:
            client_socket, client_address = s.accept()
            try:
                msg_in = get_message(client_socket)
                print(msg_in)
                msg_out = process_client_message(msg_in)
                print(msg_out)
                send_message(client_socket, msg_out)
            except json.JSONDecodeError:
                LOG.warning('Ошибка парсинга JSON')
            except ValueError:
                LOG.warning('Принято некорректное сообщение')
            except TypeError:
                LOG.error('Для отправки сообщения нужен словарь с данными.')
            finally:
                client_socket.close()
    finally:
        s.close()


if __name__ == '__main__':
    main()
