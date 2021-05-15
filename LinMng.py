import os


class LinMng: #класс менеджера для Linux

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
                os.system('touch ' + name)
                return "Ok"
            else:
                return "Such file already exists"
        elif options[0] == "-d":
            name = ' '.join(options[1:])
            name.replace("\\", "\\\\")
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if not os.path.isdir(name):
                os.system('mkdir ' + name)
                return "Ok"
            else:
                return "Such directory already exists"
        else:
            return "Wrong input format"

    def delete(self, options): #удаление файла/папки
        if options[0] == "-f":
            name = ' '.join(options[1:])
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isfile(name):
                os.system('rm ' + name)
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
                    os.system('rmdir ' + name)
                    return "Ok"
                except OSError:
                    return "Directory is not empty"

            else:
                return "Such directory does not exist"
        else:
            return "Wrong input format"


    def move(self, options): #перемещение файла/папки
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
                    os.system('mv ' + last_place + ' ' + new_place)
                    return "Ok"
                else:
                    return "Final directory does not exist"
            else:
                return "Such file does not exist"
        else:
            return "Wrong input format"

    def copy(self, options): #копирование файла/папки
        name = ' '.join(options).split("\"")
        if len(name) == 5:
            last_place = name[1]
            new_place = name[3]
            if not (self.root in last_place):
                last_place = os.path.join(self.path, last_place)
            new_place = self.root + "\\" + new_place
            if not (self.root in new_place):
                new_place = os.path.join(self.path, new_place)
            if os.path.isfile(last_place):
                if os.path.isdir(new_place):
                    os.system('cp ' + last_place + ' ' + new_place)
                    return "Ok"
                else:
                    return "Final directory does not exist"
            else:
                return "Such file does not exist"
        else:
            return "Wrong input format"

    def rename(self, options): #переименование файла/папки
        self.move(options)

    def change_directory(self, options): #переход в другую директорию
        name = ' '.join(options)
        if name == "..":
            substr = self.path.partition(self.root)[2]
            if substr.count("\\") == 0:
                return "It is a root directory"
            else:
                os.popen('cd ..')
                os.chdir(os.path.expandvars(".."))
                self.path = os.getcwd()
                return "Ok"
        else:
            if (name in self.path):
                return "Refused"
            if not(self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isdir(name):
                os.popen('cd ' + name)
                os.chdir(os.path.expandvars(name))
                self.path = os.getcwd()
                self.print_content()
                return "Ok"
            else:
                return "Such directory does not exist"

    def print_content(self): #содержимое папки
        return '; '.join(os.listdir(self.path))

    def print_path(self): #текущий путь
        return "Current path:" + self.path.replace(self.root, '\\')