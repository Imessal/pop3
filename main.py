import socket
import ssl
import re

host = 'pop.yandex.ru'
port = 995
buffer_size = 1024
user_name = 'rikmil0s'
password = 'rik123'


def send(sock: socket.socket, command):
    sock.sendall(f'{command}\n'.encode())
    # return sock.recv(buffer_size)
    sock.settimeout(1)
    res = b''
    try:
        while True:
            message = sock.recv(buffer_size)
            if not message:
                break
            res += message
    finally:
        # return sock.recv(buffer_size).decode()
        return res.decode()


def work():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
        sock.connect((host, port))
        print(sock.recv(buffer_size).decode())

        print(send(sock, f"USER {user_name}"))
        print(send(sock, f"PASS {password}"))

        print(send(sock, "STAT"))
        print(send(sock, 'LIST'))
        answer = (send(sock, 'RETR 1'))
        print(answer)
        # print(send(sock, 'TOP 7 0'))
        boundary_rg = r'Content-Type: multipart/mixed;.\s+boundary="(.*?)"'
        boundary = re.findall(boundary_rg, answer)[0]
        print('\n'.join(answer.split(f'--{boundary}')[1:-1]))
        # print(answer.split(boundary))


if __name__ == '__main__':
    work()
