from GoAhead_vuln_tool.main_goahead import main as goAheadTool_start
from OpenCam_RTSP.mainOpenCam import main as openCamTool_start
from files.settings import get_settings
from os import system, name
import json

def get_version():
    settings_parameters = get_settings()
    return settings_parameters["settings"]["info"]["version"]

banner = f"""

    ██╗ ██████╗  ██████╗ ██████╗     ██████╗ ██╗   ██╗██████╗ ██╗  ██╗ ██████╗ 
    ██║██╔════╝ ██╔═══██╗██╔══██╗    ██╔══██╗██║   ██║██╔══██╗██║ ██╔╝██╔═══██╗
    ██║██║  ███╗██║   ██║██████╔╝    ██████╔╝██║   ██║██████╔╝█████╔╝ ██║   ██║
    ██║██║   ██║██║   ██║██╔══██╗    ██╔═══╝ ██║   ██║██╔═══╝ ██╔═██╗ ██║   ██║
    ██║╚██████╔╝╚██████╔╝██║  ██║    ██║     ╚██████╔╝██║     ██║  ██╗╚██████╔╝
    ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                                                                               
     ██████╗ █████╗ ███╗   ███╗██╗  ██╗ █████╗  ██████╗██╗  ██╗                
    ██╔════╝██╔══██╗████╗ ████║██║  ██║██╔══██╗██╔════╝██║ ██╔╝                
    ██║     ███████║██╔████╔██║███████║███████║██║     █████╔╝                 
    ██║     ██╔══██║██║╚██╔╝██║██╔══██║██╔══██║██║     ██╔═██╗                 
    ╚██████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗██║  ██╗                
     ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                
                                                                               
    ███╗   ███╗██╗   ██╗██╗  ████████╗██╗████████╗ ██████╗  ██████╗ ██╗        
    ████╗ ████║██║   ██║██║  ╚══██╔══╝██║╚══██╔══╝██╔═══██╗██╔═══██╗██║        
    ██╔████╔██║██║   ██║██║     ██║   ██║   ██║   ██║   ██║██║   ██║██║        
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║   ██║   ██║   ██║██║   ██║██║        
    ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║   ██║   ╚██████╔╝╚██████╔╝███████╗   
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝   
                                                                               

    Версия:{get_version()}
"""

def clean_screen():
    system('cls' if name == 'nt' else 'clear')

INVALID_INPUT = "Неправильное значение"

def init():
    while True:
        print(f"""{banner}
              
            1) Взлом через дырку в камерах "GoAhead")   
            2) Сбор открытых камер работающие по RTSP
            

            0) Выход
            
                """)    
        
        try: input_action = int(input("Выбери действие: "))
        except ValueError:
            print(INVALID_INPUT)
            continue

        if input_action <= 2 or input_action <= 0:
            print("Понял")

            if input_action == 1:
                clean_screen()
                goAheadTool_start()
                break

            elif input_action == 2:
                clean_screen()
                openCamTool_start()
                break

            else:
                break
        else:
            print(INVALID_INPUT)
            continue

if __name__ == "__main__":
    init()

ex = input("Нажми Enter для закрытия окна")