### Импорт библиотек
from os import system, name
import GoAhead_vuln_tool.goAhead_functions as mainfuncs
from time import sleep
from files.settings import init_settings_goahead_menu, get_settings
INVALID_INPUT = "Неправильное значение"

def action_on_invalid_input(sleep_time):
    print(INVALID_INPUT)
    sleep(sleep_time)

def init():
    
    # Базовые настройки
    settings = get_settings()
    search_request = 'realm="GoAhead"' # Запрос
    API_KEY = settings["settings"]["Shodan_API_key"] # API ключ
    page = settings["settings"]["page"]
    Timeout = settings["settings"]["Timeout"]
    country = settings["settings"]["Country"]
    search_request = f'realm="GoAhead" country:"{country}"' if country != "" else 'realm="GoAhead"'
    

    banner = """
    ██╗ ██████╗  ██████╗ ██████╗     ██████╗ ██╗   ██╗██████╗ ██╗  ██╗ ██████╗                        
    ██║██╔════╝ ██╔═══██╗██╔══██╗    ██╔══██╗██║   ██║██╔══██╗██║ ██╔╝██╔═══██╗                       
    ██║██║  ███╗██║   ██║██████╔╝    ██████╔╝██║   ██║██████╔╝█████╔╝ ██║   ██║                       
    ██║██║   ██║██║   ██║██╔══██╗    ██╔═══╝ ██║   ██║██╔═══╝ ██╔═██╗ ██║   ██║                       
    ██║╚██████╔╝╚██████╔╝██║  ██║    ██║     ╚██████╔╝██║     ██║  ██╗╚██████╔╝                       
    ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝ ╚═════╝                        
                                                                                                    
     ██████╗ █████╗ ███╗   ███╗██╗  ██╗ █████╗  ██████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     
    ██╔════╝██╔══██╗████╗ ████║██║  ██║██╔══██╗██╔════╝██║ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    ██║     ███████║██╔████╔██║███████║███████║██║     █████╔╝        ██║   ██║   ██║██║   ██║██║     
    ██║     ██╔══██║██║╚██╔╝██║██╔══██║██╔══██║██║     ██╔═██╗        ██║   ██║   ██║██║   ██║██║     
    ╚██████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗██║  ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗
     ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝


    Взлом камер через уязвимость в камерах GoAhead

    """

    main_menu = f"""{banner}

            1) Получение данных о камерах через API
            2) Проверка IP адресов камер на валидность
            3) Проверка камеры на уязвимость
            4) Получение списка с данными о камере
            5) Все вместе

            99) Настройки
            0) Выход

            """

    def print_main_menu():
        system('cls' if name == 'nt' else 'clear')
        print(main_menu)

    while True:
        print_main_menu()

        try: action_input = int(input("Выбери действие: "))
        except ValueError:
            action_on_invalid_input(2)
            continue

        if action_input <= 5 or action_input <= 0 or action_input == 99:
            print("Понял")

            if action_input == 99:
                init_settings_goahead_menu()

                break

            elif action_input <= 5 or action_input <= 0:
                break

        else:
            action_on_invalid_input(2)
            continue
        

    if action_input == 1:
        mainfuncs.get_api_results(API_KEY, search_request, page) # Получаем данные с API

    elif action_input == 2: # Пингуем адреса чтобы отбросить фейки с хонипотами и записываем REAAL адреса в файл
        mainfuncs.ping_ips_for_valid(Timeout)

    elif action_input == 3: # Получаем IP адреса с имеющиеся уязвимостью и если нашли то записываем в файл
        mainfuncs.find_vuln_cameras(Timeout)

    elif action_input == 4: # Получаем содержимое файла с паролями
        mainfuncs.get_creditionals_from_vuln_ips(Timeout)

    elif action_input == 5: # Пункт все вместе
        mainfuncs.all_in_one(API_KEY, search_request, page, Timeout)

    elif action_input == 0:
        exit()

def main():
    while True:
        exit_code = init()