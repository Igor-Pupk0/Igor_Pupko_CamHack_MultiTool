### Импорт библиотек

import requests
import json
from time import sleep

import socket

### Базовые переменные

def set_variables(FILES_FOLDER):
    global API_RESULTS_FILE, PINGED_IP_ADRESSES_FILE, VULNERABLE_IP_ADRESSES_FILE
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

