import time
import shutil
import pyautogui
import random
import os

def fake_delete_server_file(filename):
    print(f"Удаление файла с сервера: {filename}")


def mouse():
    randx = random.choice([-2, 2])
    randy = random.choice([-2, 2])
    pyautogui.move(randx, randy)


max_iterations = 10

for i in range(max_iterations):
    delay = random.uniform(0.1, 1000.1234567)

    # Конфигурационные файлы
    fake_delete_server_file(f"config_{delay}.json")
    mouse()
    print(f"Done!")
    mouse()
    delay = random.uniform(0.1, 1000.1234567)
    mouse()
    fake_delete_server_file(f"settings_{delay}.yaml")
    print(f"Done!")
    mouse()
    delay = random.uniform(0.1, 1000.1234567)
    fake_delete_server_file(f"preferences_{delay}.ini")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)

    # Логи и журналы
    fake_delete_server_file(f"server_log_{delay}.log")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)
    fake_delete_server_file(f"error_log_{delay}.log")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)
    fake_delete_server_file(f"access_log_{delay}.log")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)

    # Данные пользователей
    fake_delete_server_file(f"profile_{delay}.dat")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)
    mouse()
    fake_delete_server_file(f"cache_{delay}.bin")
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)
    fake_delete_server_file(f"temp_{delay}.tmp")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)
    mouse()

    # Системные файлы
    fake_delete_server_file(f"backup_{delay}.bak")
    mouse()
    print(f"Done!")
    delay = random.uniform(0.1, 1000.1234567)
    mouse()
    fake_delete_server_file(f"session_{delay}.ses")
    mouse()
    print(f"Done!")
    mouse()
    delay = random.uniform(0.1, 1000.1234567)
    fake_delete_server_file(f"stats_{delay}.csv")
    mouse()
    print(f"Done!")
time.sleep(2)
with open("deleted.txt", "w") as f:
    f.write("virus deleted!")
source = "deleted.txt"
destination = os.path.expandvars("%appdata%/deleted.txt")
shutil.move(source, destination)