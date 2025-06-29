import threading
import json 
import cv2
from time import sleep
import time
from files.baseFunctions import get_api_results, ping_ips_for_valid, set_variables


### Базовые переменные
FILES_FOLDER = "OpenCam_RTSP/files"
API_RESULTS_FILE = f"{FILES_FOLDER}/api_results.json"
PINGED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/pinged_ips.json"
OPENED_IP_ADRESSES_FILE = f"{FILES_FOLDER}/opened_ips.json"
OPENED_IP_ADRESSES_FILE_CLEAR = f"{FILES_FOLDER}/opened_ips.txt"
set_variables(FILES_FOLDER)



def check_rtsp_stream(ip, timeout):
    result = {'open': False}  # словарь для хранения результата
    event = threading.Event()  # событие для синхронизации

    def worker():
        try:
            # Формируем корректный RTSP URL
            rtsp_url = f"rtsp://{ip}"
            
            # Пробуем открыть поток
            cap = cv2.VideoCapture(rtsp_url)
            
            # Устанавливаем таймаут для чтения
            start_time = time.time()
            while not event.is_set():
                if cap.isOpened():
                    result['open'] = True
                    break
                
                # Проверяем таймаут внутри потока
                if time.time() - start_time > timeout:
                    break
                
                # Даем время для инициализации
                time.sleep(0.1)
        except Exception as e:
            print(f"Ошибка при проверке {ip}: {e}")
        finally:
            # Всегда освобождаем ресурсы
            if 'cap' in locals():
                cap.release()
            event.set()  # сигнализируем о завершении

    thread = threading.Thread(target=worker)
    thread.daemon = True  # делаем поток демоном
    thread.start()
    
    # Ждем завершения потока с таймаутом
    event.wait(timeout + 1)  # даем дополнительную секунду
    
    # Если поток все еще работает, прерываем
    if thread.is_alive():
        print(f"Таймаут достигнут для {ip}, прерывание проверки")
        event.set()  # просим поток завершиться
        thread.join(timeout=1)  # даем время на завершение

    return result['open']

def check_open_camera(timeout):
    # Проверка входных параметров
    if timeout <= 0:
        raise ValueError("Таймаут должен быть положительным числом")

    try:
        with open(PINGED_IP_ADRESSES_FILE, "r", encoding="utf-8") as f:
            pinged_ips = json.load(f)
    except FileNotFoundError:
        print(f"Файл не найден: {PINGED_IP_ADRESSES_FILE}")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка формата JSON в файле: {e}")
        return

    opened_ips = []
    total = len(pinged_ips)
    
    if total == 0:
        print("Нет IP-адресов для проверки")
        with open(OPENED_IP_ADRESSES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return

    print(f"Начинаем проверку {total} камер, таймаут: {timeout} сек")

    for i, device in enumerate(pinged_ips, 1):
        ip = device.get('ip', '')
        port = device.get('port', '')
        
        if not ip or not port:
            print(f"Пропуск невалидной записи: {device}")
            continue
            
        host = f"{ip}:{port}"
        print(f"Проверка ({i}/{total}): {host}", end=" ", flush=True)
        
        try:
            # Проверяем RTSP-поток с детализацией ошибок
            if check_rtsp_stream(host, timeout):
                print("[ДОСТУПНА]")
                opened_ips.append(device)
            else:
                print("[НЕДОСТУПНА]")
        except Exception as e:
            print(f"[ОШИБКА: {type(e).__name__}]")
            # Для диагностики можно добавить логирование исключений
            # import traceback; traceback.print_exc()

    print(f"Найдено доступных камер: {len(opened_ips)}/{total}")

    with open(OPENED_IP_ADRESSES_FILE, "w", encoding="utf-8") as f:
        json.dump(opened_ips, f, indent=2)  # Добавляем форматирование для читаемости

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
