### Импорт библиотек

import threading
import requests
import json
import requests.exceptions
import socket
import cv2
from time import sleep

### Базовые переменные
FILES_FOLDER = "OpenCam_RTSP/files"
API_RESULTS_FILE = f"{FILES_FOLDER}/api_results.json"
PINGED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/pinged_ips.json"
OPENED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/opened_ips.json"
OPENED_IP_ADRESSES_FILE_CLEAR = f"{FILES_FOLDER}/opened_ips.txt"

### Получаем данные с API
def get_api_results(API_KEY, search_request, page):

    with open(API_RESULTS_FILE, "w") as file:

        response = requests.get(f"https://api.shodan.io/shodan/host/search?key={API_KEY}&query={search_request}&page={page}")
        file.write(response.text)

### Пингуем адреса чтобы отбросить фейки с хонипотами и записываем REAAL адреса в файл

def ping_ips_for_valid(Timeout):
    js = open(API_RESULTS_FILE, "r", encoding="utf-8")
    try:
        js_data = json.loads(js.read())
    except json.decoder.JSONDecodeError:
        print("Не удалось распознать инфо в API, может ты не указал или указал неправильный ключ API?")
        sleep(5)
        js.close()
        exit()

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

    def ping(host,port,timeout=Timeout): # Пинг по порту
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)

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


def check_rtsp_stream(ip, timeout):
    result = {'open': False}  # словарь для хранения результата

    def worker():
        cap = cv2.VideoCapture(f"rtsp://{ip}/")
        result['open'] = cap.isOpened()
        cap.release()

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout=timeout)  # ждем завершения потока с таймаутом

    # Проверяем, завершился ли поток
    if thread.is_alive():
        print("Timeout reached, stream check aborted:", ip)
        return False  # если поток не завершился, считаем, что поток закрыт

    return result['open']  # возвращаем результат проверки


def check_open_camera(Timeout):
    read_file = open(PINGED_IP_ADRESSES_FILE, "r", encoding="utf-8")

    pinged_ips_json = json.load(read_file)
    read_file.close()

    writefile = open(OPENED_IP_ADRESSES_FILE, "w", encoding="utf-8")
        
    count_ips = 0
    for i, o in enumerate(pinged_ips_json):

        pinged_ip_host = f"{pinged_ips_json[i]['ip']}:{pinged_ips_json[i]['port']}"

        if check_rtsp_stream(pinged_ip_host, Timeout):
            print("OPENED:", pinged_ip_host)
            count_ips += 1

            if count_ips == 1:
                opened_ip_address_json = [pinged_ips_json[i]]

            opened_ip_address_json += [pinged_ips_json[i]]

        else:
            print("CLOSED:", pinged_ip_host)

    opened_ip_address_json_list = list(opened_ip_address_json)
    json.dump(opened_ip_address_json_list, writefile, separators=(',', ':'))

    writefile.close()


def json_to_txt():
    read_file = open(OPENED_IP_ADRESSES_FILE, 'r', encoding="utf-8")

    js_data = json.load(read_file)

    read_file.close()

    writefile = open(OPENED_IP_ADRESSES_FILE_CLEAR, 'w', encoding="utf-8")

    data_to_write = ''

    for i in js_data:
        data_to_write += f"{i['ip']}:{i['port']}, city:{i['city']}\n"

    writefile.write(data_to_write)
    writefile.close()




### Оптимизированный вариант пункта "Все вместе"

def all_in_one(API_KEY, search_request, page, Timeout):
    get_api_results(API_KEY, search_request, page)
    ping_ips_for_valid(Timeout)
    check_open_camera(Timeout)
    json_to_txt()
