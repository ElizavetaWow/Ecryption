import os


class WinMng:

    def __init__(self, path):
        """Constructor"""
        self.path = path
        if os.path.exists(path):
            os.chdir(path)
        else:
            self.path = os.getcwd()
        self.root = path

    def create(self, options):
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

    def delete(self, options):
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

    def change_directory(self, options):
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
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isdir(name):
                os.chdir(name)
                self.path = os.getcwd()
                self.print_content()
                return "Ok"
            else:
                return "Such directory does not exist"

    def open(self, options):
        if options[0] == "-r":
            name = ' '.join(options[1:])
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isfile(name):
                text_file = open(name, "r")
                for i in text_file.readlines():
                    print(i)
                text_file.close()
                return "Ok"
            else:
                return "Such file does not exist"
        elif options[0] == "-w":
            name = ' '.join(options[1:])
            if not (self.root in name):
                name = os.path.join(self.path, name)
            text_file = open(name, "w")
            text = input("Write text for file: \n")
            text_file.write(text)
            text_file.close()
            return "Ok"
        else:
            return "Wrong input format"

    def move(self, options):
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

    def copy(self, options):
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
                    os.system('copy ' + last_place + ' ' + new_place)
                    return "Ok"
                else:
                    return "Final directory does not exist"
            else:
                return "Such file does not exist"
        else:
            return "Wrong input format"

    def rename(self, options):
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

    def print_content(self):
        for i in os.listdir(self.path):
            print(i)
