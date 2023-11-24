import socket
import time

def savescores(req):
    username = req[1]
    score = req[2]
    f = open("scores.txt", "a")
    f.write(f"{username} : {score}\n")
    f.close()

def read_scores():
    """Reads Scores from Scores.txt and returns a dictionary containing key-value pairs of usernames-scores"""
    scores = {}
    with open(f"scores.txt") as f:
        for line in f:
            (key, val) = line.split(" : ")
            key = key.strip()
            val = val.strip()
            scores[(key)] = val
    return scores

def sendscores():
    scores = read_scores()
    scores_str = ""
    for username in scores.keys():
        scores_str = scores_str + f"{username}:{scores[username]}#"
    return scores_str


host = "192.168.1.127"
port = 55000
s = socket.socket()
s.bind((host, port))
while True:
    try:
        s.listen(1)
        conn, addr = s.accept()
        req = conn.recv(2048).decode()
        timer_start = time.perf_counter()
        print(f'Received Request.')
        req = req.split("+")
        if req[0] == "REQ=POSTSCORES":
            savescores(req)
        elif req[0] == "REQ=GETSCORES":
            conn.send(sendscores().encode())
        elif req[0] == "REQ=CHECKCONN":
            conn.send("OK".encode())
        conn.close()
        print(f'Request Served. (Served In: {(time.perf_counter() - timer_start) * 1000:.2f} ms)')
    except socket.error:
        print(f'Socket-Error occured!')
        conn.close()
        False