"""
Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает результат из байтовового
типа данных в строковый без ошибок для любой кодировки операционной системы
"""

import locale, subprocess, platform


def ping(domain):
    print('{:*^30}'.format(f'ping {domain}'))

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    def_coding = locale.getpreferredencoding()
    args = ['ping', param, '3', domain]

    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        # я так и не понял зачем в этом случае раскодировать и вновь кодировать...
        # line = line.decode(def_coding).encode('utf-8')
        line = line.decode(def_coding)
        print(line, end='')


domain_list = ['yandex.ru', 'youtube.com']

[ping(domain) for domain in domain_list]