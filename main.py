import platform

import LinMng
import WinMng


def main_menu():
    print("You can do following operations: ")
    print("1.Open \n2.Rename \n3.Move and Paste \n4.Copy and Paste \n5.Delete\n6.Create files\nexit")


def ask_action():
    command = input("Print a command: ").split()
    if command[0].lower() in menuList:
        return command
    else:
        print("Such command is not found, try one more time")
        return "Not Found"


def print_instractions():
    pass


if __name__ == '__main__':
    menuList = ["create", "delete", "open", "moveto", "copypaste", "renamef", "change", "exit", "help"]
    print('Welcome to file manager!')
    platformName = platform.system()
    print('Your OS is :', platformName)
    if platformName == "Windows":
        manager = WinMng.WinMng('D:\\')
    if platformName == "Linux":
        manager = LinMng.LinMng('D:\\')
    print('Now you here : D:\\. List of elements: ')
    manager.print_content()
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
        if ans != "Ok":
            print(ans)
        else:
            print("Operation complete")
