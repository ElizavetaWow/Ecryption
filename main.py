import platform

import LinMng
import WinMng


def ask_action():
    command = input("Print a command: ").split()
    if command[0].lower() in menuList:
        return command
    else:
        print("Such command is not found, try one more time")
        return "Not Found"


def print_instractions():
    comands  = {"create type name":"Создание файла (type = \"-f\") или директории (type = \"-d\") с названием name",
                "delete type name":"Удаление файла (type = \"-f\") или директории (type = \"-d\") с названием name",
                "renamef \"lastname\" \"newname\"":"Переименование файла или директории с именем lastname на newname (двойные кавычки обязательны)",
                "change newplace":"Переход в директорию с именем newplace или на уровень выше, если newplace = \"..\"",
                "open type name":"Открытие файла для записи (type = \"-w\") или для чтения (type = \"-r\") с названием name",
                "moveto \"lastplace\" \"newplace\"":"Перемещение файла с именем lastname в директорию с именем newplace (двойные кавычки обязательны)",
                "copypaste \"lastplace\" \"newplace\"":"Копирование файла с именем lastname в директорию с именем newplace (двойные кавычки обязательны)",
                "content":"Содержимое текущей директории",
                "exit":"Завешение работы",
                "help":"Вызов справки по командам"}
    i = 1
    for k, v in comands.items():
        print(i, ') ', k, ' - ', v)
        i += 1
    
    
   


if __name__ == '__main__':
    menuList = ["create", "delete", "open", "moveto", "copypaste", "renamef", "change", "exit", "help", "content"]
    print('Welcome to file manager!')
    print("Данный файловый менеджер автоматически выбирает ОС, с которой будет работать. \nВ его функции входят создание, редактирование, удаление файлов и директорий, переход между папками, копирование и перемещение файлов.\nКорневая папка определяется в настройках (файл Settings.txt). Все возможные команды с ключами можно посмотреть по команде help.")
    platformName = platform.system()
    print('Your OS is :', platformName)
    settings = open("Settings.txt", "r")
    root = settings.readline().split("=")[1]
    if platformName == "Windows":
        manager = WinMng.WinMng(root)
    if platformName == "Linux":
        manager = LinMng.LinMng(root)
    print(f'Now you here : {root}.')
    print_instractions()
    while True:
        answer = ask_action()
        if answer == "Not Found":
            continue
        commandIndex = menuList.index(answer[0])
        if commandIndex == 0:
            ans = manager.create(answer[1:])
        if commandIndex == 1:
            ans = manager.delete(answer[1:])
        if commandIndex == 2:
            ans = manager.open(answer[1:])
        if commandIndex == 3:
            ans = manager.move(answer[1:])
        if commandIndex == 4:
            ans = manager.copy(answer[1:])
        if commandIndex == 5:
            ans = manager.rename(answer[1:])
        if commandIndex == 6:
            ans = manager.change_directory(answer[1:])
        if commandIndex == 7:
            print("Good bye")
            break
        if commandIndex == 8:
            print_instractions()
        if commandIndex == 9:
            ans = "Ok"
            manager.print_content()
        if ans != "Ok":
            print(ans)
        else:
            print("Operation complete")
