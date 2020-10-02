import os
import sys
from tkinter.ttk import Style

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


def get_dir(args):
    dir_name = args[1]
    try:
        os.mkdir(f'{dir_name}')
        return dir_name
    except FileExistsError:

        return dir_name


def check_valid_url(url):
    return url.count('.') != 0


def check_fulled_url(url):
    return 'https://' in url[8]


def check_nedded_url(url):
    return url == 'bloomberg.com' or url == 'nytimes.com'


def write_content_in_file(dir, file_name, content, list):
    with open(f'{dir}/{file_name}', 'w', encoding='UTF-8') as f:
        f.write(Fore.BLUE + content)
        list.append(file_name)


def print_content_file(dir, file_name):
    with open(f'{dir}/{file_name}', 'r') as f:
        content = f.read()
        print(Fore.BLUE + content)


def check_name_file(file_name, list):

    return file_name in list


def get_content(url):
    url_ = requests.get(url)
    content_page = BeautifulSoup(url_.content, 'html.parser')
    return content_page.text


args = sys.argv
active = True
tabs_list = []
history_page = []
page = None
last_page = None
while active:
    init()
    # пользователь вводит че хочет
    user_input = input()
    if user_input == 'exit':
        active = False
        continue
    if user_input == 'back':
        if len(history_page) == 0:
            print(' ')
            continue
        user_input = history_page.pop()
    if not check_valid_url(user_input):
        print('Error: Incorrect URL')
        page = None
        continue
    if not check_fulled_url(user_input):
        user_input = 'https://' + user_input
    history_page.append(page)
    page = get_content(user_input)
    dir = get_dir(args)
    file_name = user_input[8:-4]
    if check_name_file(file_name, tabs_list):
        print_content_file(dir, file_name)
    else:
        write_content_in_file(dir, file_name, page, tabs_list)
        print(Fore.BLUE + page)


