import platform
import WinMng, LinMng

def mainMenu():
    print("You can do following operations: ")
    print("1.Open \n2.Rename \n3.Move and Paste \n4.Copy and Paste \n5.Delete\n6.Create files\nexit")
    


if __name__ == '__main__':
    print('Welcome to file manager!\n')
    platformName = platform.system()
    print('Your OS is :', platformName, '.\n')
    if platformName == "Windows":
        manager = WinMng()
    if platformName == "Linux":
        manager = LinMng()


