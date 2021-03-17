import platform
import WinMng, LinMng

def mainMenu():
    print("You can do following operations: ")
    print("1.Open \n2.Rename \n3.Move and Paste \n4.Copy and Paste \n5.Delete\n6.Create files\nexit")

def askAction():
    command = input("Print a command: ").split()
    if command[0] in menuList:
        return command
    else:
        print("Such command is not found, try one more time")
        return "Not Found"


if __name__ == '__main__':
    menuList = ["create", "delete", "open", "move", "copy", "rename", "exit"]
    print('Welcome to file manager!\n')
    platformName = platform.system()
    print('Your OS is :', platformName, '.\n')
    if platformName == "Windows":
        manager = WinMng()
    if platformName == "Linux":
        manager = LinMng()
    while True:
        answer = askAction()
        if answer == "Not Found":
            continue
        commandIndex = menuList.index(answer[0])
        if commandIndex == 0:
            answer = manager.create(answer[1:])
            if answer != "Ok":
                print(answer)
        if commandIndex == 1:
            answer = manager.delete(answer[1:])
            if answer != "Ok":
                print(answer)
        if commandIndex == 2:
            manager.open(answer[1:])
        if commandIndex == 3:
            manager.mov(answer[1:])
        if commandIndex == 4:
            manager.cop(answer[1:])
        if commandIndex == 5:
            manager.renam(answer[1:])
        if commandIndex == 6:
            print("Good bye")
            break


