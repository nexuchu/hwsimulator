import socket

host = "192.168.1.127"
port = 55000
s = socket.socket()
s.bind((host, port))
while True:
    s.listen(1)
    conn, addr = s.accept()
    score = conn.recv(2048).decode()
    score = score.split("=")
    print(f"{score[0]} : {score[1]}")
