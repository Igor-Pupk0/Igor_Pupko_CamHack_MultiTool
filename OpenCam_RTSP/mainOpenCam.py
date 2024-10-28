### Импорт библиотек
from os import system, name
from OpenCam_RTSP import opencam_func as mainfuncs
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
        search_request_country = f'"RTSP/1.0 200 OK" country:"{country if country != "" else "RTSP/1.0 200 OK"}"'
        search_request_city = f'"RTSP/1.0 200 OK" city:"{city if city != "" else "RTSP/1.0 200 OK"}"'

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
                4) Преобразовать результат в формат txt
                5) Все вместе

                99) Настройки
                0) Выход

                """

        def print_info():
            system('cls' if name == 'nt' else 'clear')
            print(main_menu)

        while True:
            print_info()
            try: input_action = int(input("Выбери действие: "))

            except ValueError:
                print(INVALID_INPUT)
                continue
            if input_action <= 5 or input_action <= 0 or input_action == 99:
                print("Понял")

                if input_action == 99:
                    init_settings_openCam_menu()

                elif input_action <= 6 or input_action <= 0:
                    break

            else:
                print(INVALID_INPUT)
                wait(2)
                continue
            


        if input_action == 1:
            if sample_country == "False":
                print(search_request_city)
                mainfuncs.get_api_results(API_KEY, search_request_city, page)
            else:
                print(search_request_country)
                mainfuncs.get_api_results(API_KEY, search_request_country, page)


        if input_action == 2:
            mainfuncs.ping_ips_for_valid(Timeout)

        if input_action == 3:
            mainfuncs.check_open_camera(Timeout)

        if input_action == 4:
            mainfuncs.extract_data_from_json_file()

        if input_action == 5:
            if sample_country == "False":
                mainfuncs.all_in_one(API_KEY, search_request_city, page, Timeout)
            else:
                mainfuncs.all_in_one(API_KEY, search_request_country, page, Timeout)


        if input_action == 0:
            exit()



