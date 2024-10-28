### Импорт библиотек

import threading
import requests
import json
import requests.exceptions
import socket
import cv2
from time import sleep
from files.get_filtered_ip import get_api_results, ping_ips_for_valid

### Базовые переменные
FILES_FOLDER = "OpenCam_RTSP/files"
API_RESULTS_FILE = f"{FILES_FOLDER}/api_results.json"
PINGED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/pinged_ips.json"
OPENED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/opened_ips.json"
RESULT_FILE = f"{FILES_FOLDER}/result.txt"


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

def extract_data_from_json_file():
    read_file = open(OPENED_IP_ADRESSES_FILE, "r", encoding="utf-8")
    opened_ips_json = json.load(read_file)
    read_file.close()

    result_file = open(RESULT_FILE, "w", encoding="utf-8")
    for i in opened_ips_json:
        result_file.write(f"Opened cam: rtsp://{i['ip']}:{i['port']} \n")


### Оптимизированный вариант пункта "Все вместе"

def all_in_one(API_KEY, search_request, page, Timeout):
    get_api_results(API_KEY, search_request, page, output_file=API_RESULTS_FILE)
    ping_ips_for_valid(Timeout, API_file=API_RESULTS_FILE, output_file=PINGED_IP_ADRESSES_FILE)
    check_open_camera(Timeout)
    extract_data_from_json_file()
