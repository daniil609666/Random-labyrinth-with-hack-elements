import time
from tqdm import tqdm
import sys
from colorama import Fore, init
import pyautogui
import random
import shutil
import os

init()  # Инициализируем colorama

def mouse():
    randx = random.choice([-10, 10])
    randy = random.choice([-10, 10])
    pyautogui.move(randx, randy)

items = list(range(1, 21))  # Создаем список чисел от 1 до 20 более элегантным способом
print(f"{Fore.GREEN}Granting system access...")

for i in tqdm(items, desc="Access Level"):
    mouse()
    time.sleep(0.1)  # имитация работы
        
print(f"\n{Fore.GREEN}System access granted successfully!")
with open('granted.txt', 'wb') as f:
    f.write(b'hello!')
source = "granted.txt"
destination = os.path.expandvars("%appdata%/granted.txt")
shutil.move(source, destination)
sys.exit(0)  # Возвращаем 0 для успешного завершения
