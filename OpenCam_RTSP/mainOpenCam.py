### Импорт библиотек
from os import system, name
import OpenCam_RTSP.openCam_functions as mainfuncs
from time import sleep as wait
from files.settings import init_settings_openCam_menu, get_settings

INVALID_INPUT = "Неправильное значение"

def main():
    while True:

        settings = get_settings()
        city = settings["settings"]["city"]
        API_KEY = settings["settings"]["Shodan_API_key"] # API ключ
        page = settings["settings"]["page"]
        Timeout = settings["settings"]["Timeout"]
        country = settings["settings"]["Country"]
        sample_country = settings["settings"]["sample_country"]
        search_request_country = f'"has_screenshot:True RTSP/1.0 200 OK" country:"{country if country != "" else "has_screenshot:True 'RTSP/1.0 200 OK'"}"'
        search_request_city = f'has_screenshot:True "RTSP/1.0 200 OK" city:"{city if city != "" else "has_screenshot:True 'RTSP/1.0 200 OK' "}"'

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


        Обнаружение открытых камер

        """

        main_menu = f"""{banner}

                1) Получение данных о открытых камерах через API
                2) Проверка IP адресов камер на валидность
                3) Проверка открытости камер
                4) Преобразовать вывод json в txt
                5) Все вместе

                99) Настройки
                0) Выход

                """

        def print_info():
            system('cls' if name == 'nt' else 'clear')
            print(main_menu)

        while True:
            print_info()
            try: inp = int(input("Выбери действие: "))

            except ValueError:
                print(INVALID_INPUT)
                continue
            if inp <= 5 or inp <= 0 or inp == 99:
                print("Понял")

                if inp == 99:
                    init_settings_openCam_menu()

                elif inp <= 6 or inp <= 0:
                    break

            else:
                print(INVALID_INPUT)
                wait(2)
                continue
            


        ### Получаем данные с API
        match inp:
            case 1:
                if sample_country == "False":
                    print(search_request_city)
                    mainfuncs.get_api_results(API_KEY, search_request_city, page)
                else:
                    print(search_request_country)
                    mainfuncs.get_api_results(API_KEY, search_request_country, page)

            ### Пингуем адреса чтобы отбросить фейки с хонипотами и записываем REAAL адреса в файл

            case 2:
                mainfuncs.ping_ips_for_valid(Timeout)

            case 3:
                mainfuncs.check_open_camera(Timeout)

            case 4:
                mainfuncs.json_to_txt()

            case 5:
                if sample_country == "False":
                    mainfuncs.all_in_one(API_KEY, search_request_city, page, Timeout)
                else:
                    mainfuncs.all_in_one(API_KEY, search_request_country, page, Timeout)


            case 0:
                exit()



