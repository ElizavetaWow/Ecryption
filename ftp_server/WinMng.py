import os


class WinMng:  #класс менеджера для Windows

    def __init__(self, path):
        """Constructor"""
        self.path = path
        if os.path.exists(path):
            os.chdir(path)
        else:
            self.path = os.getcwd()
        self.root = path

    def create(self, options): #создание файла/папки
        if options[0] == "-f":
            name = ' '.join(options[1:])
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if not os.path.isfile(name):
                text_file = open(name, "w")
                text_file.close()
                return "Ok"
            else:
                return "Such file already exists"
        elif options[0] == "-d":
            name = ' '.join(options[1:])
            name.replace("\\", "\\\\")
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if not os.path.isdir(name):
                os.makedirs(name)
                return "Ok"
            else:
                return "Such directory already exists"
        else:
            return "Wrong input format"

    def delete(self, options):  #удаление файла/папки
        if options[0] == "-f":
            name = ' '.join(options[1:])
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isfile(name):
                os.remove(name)
                return "Ok"
            else:
                return "Such file does not exist"
        elif options[0] == "-d":
            name = ' '.join(options[1:])
            name.replace("\\", "\\\\")
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isdir(name):
                try:
                    os.rmdir(name)
                    return "Ok"
                except OSError:
                    return "Directory is not empty"

            else:
                return "Such directory does not exist"
        else:
            return "Wrong input format"

    def change_directory(self, options):  #переход в другую директорию
        name = ' '.join(options)
        if name == "..":
            substr = self.path.partition(self.root)[2]
            if substr.count("\\") == 0:
                return "It is a root directory"
            else:
                os.chdir("..")
                self.path = os.getcwd()
                return "Ok"
        else:
            if (name in self.path):
                return "Refused"
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isdir(name):
                os.chdir(name)
                self.path = os.getcwd()
                return "Ok"
            else:
                return "Such directory does not exist"


    def move(self, options):  #перемещение файла/папки
        name = ' '.join(options).split("\"")
        if len(name) == 5:
            last_place = name[1]
            new_place = name[3]
            if not (self.root in last_place):
                last_place = os.path.join(self.path, last_place)
            if not (self.root in new_place):
                new_place = os.path.join(self.path, new_place)
            if os.path.isfile(last_place):
                if os.path.isdir(new_place):
                    os.replace(last_place, new_place)
                    return "Ok"
                else:
                    return "Final directory does not exist"
            else:
                return "Such file does not exist"
        else:
            return "Wrong input format"

    def copy(self, options):  #копирование файла/папки
        name = ' '.join(options).split("\"")
        if len(name) == 5:
            last_place = name[1]
            new_place = name[3]
            if not (self.root in last_place):
                last_place = os.path.join(self.path, last_place)
            new_place = self.root +"\\"+ new_place
            if not (self.root in new_place):
                new_place = os.path.join(self.path, new_place)
            if os.path.isfile(last_place):
                if os.path.isdir(new_place):
                    os.system('copy ' + last_place + ' ' + new_place+'')
                    return "Ok"
                else:
                    return "Final directory does not exist"
            else:
                return "Such file does not exist"
        else:
            return "Wrong input format"

    def rename(self, options):  #переименование файла/папки
        name = ' '.join(options).split("\"")
        if len(name) == 5:
            last_name = name[1]
            new_name = name[3]
            if not (self.root in last_name):
                last_name = os.path.join(self.path, last_name)
            if not (self.root in new_name):
                new_name = os.path.join(self.path, new_name)
            if os.path.isfile(last_name):
                if not os.path.isfile(new_name):
                    os.rename(last_name, new_name)
                    return "Ok"
                else:
                    return "Such file already exists"
            else:
                return "Such file does not exist"
        else:
            return "Wrong input format"

    def print_content(self):  #содержимое папки
        return '; '.join(os.listdir(self.path))

    def print_path(self):  #текущий путь
        return "Current path:" + self.path.replace(self.root, '\\')
