### Импорт библиотек
from os import system, name
from time import sleep
import json

SETTINGS_FILE = "files/settings.json" # Путь к файлу с настройками
SETTINGS_FILE_SOURCE = "files/settings_example.json" # Путь к шаблону с настройками

def get_settings():
    try:
        js = open(SETTINGS_FILE, "r", encoding="utf-8") # Получение данных с настроек
    except FileNotFoundError:

        settings_source = open(SETTINGS_FILE_SOURCE, "r", encoding="utf-8")
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            file.write(settings_source.read())
        
        js = open(SETTINGS_FILE, "r", encoding="utf-8") # Получение данных с настроек


    settings_parameters = json.loads(js.read())
    js.close()
    return settings_parameters

def write_settings(settings):
    file = open(SETTINGS_FILE, "w")
    file.write(json.dumps(settings))
    file.close()

country_codes = ["",  "AU","MG","AT","MW","AZ","MY","AL","ML","DZ","UM","AI","MV","AO",
            "AD","MP","AQ","MA","AG","MQ","AN","MH","MO","MX","AR","FM","AM","MZ","AW",
            "MD","AF","MC","BS","MN","BD","MS","BB","MM","BH","NA","BZ","NR","BY","NP",
            "BE","NE","BJ","NG","BM","NL","BG","NI","BO","NU","BW","NZ","BR","NC","IO",
            "NO","BN","NF","BV","AE","BF","OM","BI","CK","BT","MI","VU","IM","VA","CX",
            "GB","SH","HU","WK","VE","PK","VI","PW","VG","PA","AS","PG","TP","PY","VN",
            "PE","GA","PN","HT","PL","GY","PT","GM","PR","GH","NT","GP","RE","GT","RU",
            "GF","RW","GN","RO","GW","SV","DE","SM","GI","ST","HN","SA","GD","SZ","GL",
            "SC","GR","PM","GE","SN","GU","VC","DK","KN","DJ","LC","JT","SG","DM","SY",
            "DO","SK","EG","SB","ZR","SO","ZM","SD","EH","SR","WS","SL","ZW","US","IL",
            "HK","IN","TJ","ID","TH","JO","TW","IQ","TZ","IR","TC","IE","TG","IS","TK",
            "ES","TO","IT","tt","YE","TV","CV","TN","KZ","TM","KY","tr","KH","UG","CM",
            "UZ","CA","UA","QA","WF","KE","UY","CY","FO","KI","FJ","CN","PH","CC","FI",
            "CO","FK","KM","FR","CG","PF","KP","TF","KR","HM","CR","CF","CI","td","CU",
            "CZ","KW","CL","KG","CH","LA","SE","LV","SJ","LT","LK","LS","EC","LR","GQ",
            "LB","EE","LY","ET","LI","YU","LU","ZA","MU","JM","MR","JP", "MT"] # Коды разлиных стран


settings_banner = """
    ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
    ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
    ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
    ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
    ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝"""


INVALID_INPUT = "Неправильное значение"

def action_on_invalid_input(sleep_time):
    print(INVALID_INPUT)
    sleep(sleep_time)


def init_settings_goahead_menu():

    settings = get_settings()
    page = settings["settings"]["page"]
    Timeout = settings["settings"]["Timeout"]
    country = settings["settings"]["Country"]


    settings_menu = f"""
        {settings_banner}

        1) Указать API Shodan (Необходимо)
        2) Выбор страны (поставлено "{country if country != "" else "никакая"}")
        |    3) Посмотреть коды стран (открыть файл)

        4) Выбор страницы для API (поставлено {page})
        5) Настроить Timeout хоста в секундах (поставлено {Timeout}, может зависить от кол-во камер в итоге)

        0) Выход

        """
    
    print(settings_menu)
    
    try: settings_input = int(input("Выбери действие: "))
    except ValueError:
        action_on_invalid_input(2)
        pass
    
    if settings_input == 2:
        fake_country = True
        input_country = input("Введи двухзначный код страны (Пример: Польша - PL, США - US): ")

        for i in country_codes:

            if input_country.upper() == i.upper():
                fake_country = False

        if fake_country == True:
            action_on_invalid_input(2)

        else:
            settings["settings"]["Country"] = input_country.upper()
            write_settings(settings)

        
    elif settings_input == 3:
        system("notepad GoAhead_vuln_tool/countries_codes.txt")
        pass

    elif settings_input == 4:
        try: settings["settings"]["page"] = int(input("Введи номер страницы (если такой страницы не будет то результата не буде): "))
        except ValueError:
            action_on_invalid_input(2)
            

        write_settings(settings)

    elif settings_input == 5:
        try: settings["settings"]["Timeout"] = int(input("Введи сколько секунд будет выделяться на ожидание ответа от хоста: "))
        except ValueError:
            action_on_invalid_input(2)
            

        write_settings(settings)
        
    elif settings_input == 1:
        settings["settings"]["Shodan_API_key"] = input("Введите API ключ от аккаунта на Shodan, правильность ключа на твоей же совести: ")
        write_settings(settings)

    elif settings_input == 0:
        pass


def init_settings_openCam_menu():

    # Получение настроек
    settings = get_settings()
    city = settings["settings"]["city"] # Город
    page = settings["settings"]["page"]
    Timeout = settings["settings"]["Timeout"]
    country = settings["settings"]["Country"]
    sample_country = settings["settings"]["sample_country"]
    sample = "стране"

    openCam_settings_menu = f"""
    {settings_banner}

            1) Указать API Shodan (Необходимо)
            2) Выбор страны (поставлено "{country if country != "" else "никакая"}")
            |    3) Посмотреть коды стран (открыть файл)

            4) Выбор города (на английском, поставлен {city if city != "" else "никакой"})
            5) Выбор страницы для API (поставлено {page})
            6) Настроить Timeout хоста в секундах (поставлено {Timeout}, может зависить от кол-во камер в итоге)
            7) Выборка по городу или стране (поставлена по {sample if sample_country == "True" else "городу"})

            
            0) Выход

            """
    
    print(openCam_settings_menu)
    
    try:
        settings_inp = int(input("Выбери действие: "))
    except ValueError:
        action_on_invalid_input(2)
    
    if settings_inp == 2:
        fake_country = True
        input_country = input("Введи двухзначный код страны (Пример: Польша - PL, США - US): ")

        for i in country_codes:

            if input_country.upper() == i.upper():
                fake_country = False

        if input_country == "ДНР":
            print("Critical Error: 'ДНР' Невозможно взломать ")
            sleep(2)
            print("Великий ДНР конечно СТРАНА! Но ВЕЛИКИЙ Пенис Душилин обезопасил ДНР настолько, что даже Игорь Пупко не способен взломать камеры тут")
            sleep(10)

        if fake_country == True:
            print("Вирт страна, такой нет")
            action_on_invalid_input(4)

        else:
            settings["settings"]["Country"] = input_country.upper()
            write_settings(settings)

        
    elif settings_inp == 3:
        system("notepad GoAhead_vuln_tool/countries_codes.txt")

    elif settings_inp == 4:
        settings["settings"]["city"] = input("Введи название города на английском (Пример: Москва - Moscow, Красноярск - Krasnoyarsk): ").capitalize()
        write_settings(settings)

    elif settings_inp == 5:

        try:
            settings["settings"]["page"] = int(input("Введи номер страницы (если такой страницы не будет то результата не буде): "))
        except ValueError:
            print("Неправильно введено значение, оно осталось прежним")
            action_on_invalid_input(2)

        write_settings(settings)

    elif settings_inp == 6:
        try:
            settings["settings"]["Timeout"] = int(input("Введи сколько секунд будет выделяться на ожидание ответа от хоста: "))
        except ValueError:
            print("Неправильно введено значение, оно осталось прежним")
            action_on_invalid_input(2)

        write_settings(settings)

    elif settings_inp == 7:
        city = input("Введи по какому признаку будет проводиться выборка камер (Г - по городу, С - стране): ")
        
        if city.upper() == "С" or city.upper() == "C":
            settings["settings"]["sample_country"] = "True"
            write_settings(settings)

        elif city.upper() == "Г":
            settings["settings"]["sample_country"] = "False"
            write_settings(settings)

        else:
            print("Неправильно введено значение, оно осталось прежним")
            action_on_invalid_input(2)

    elif settings_inp == 1:
        settings["settings"]["Shodan_API_key"] = input("Введите API ключ от аккаунта на Shodan, правильность ключа на твоей же совести: ")
        write_settings(settings)

    elif settings_inp == 0:
        pass