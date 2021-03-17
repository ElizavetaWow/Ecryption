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
            if not os.path.isfile(os.path.join(self.path, name)):
                text_file = open(os.path.join(self.path, name), "w")
                text_file.close()
                return "Ok"
            else:
                return "Such file already exists"
        elif options[0] == "-d":
            name = ' '.join(options[1:])
            name.replace("\\", "\\\\")
            if not os.path.isdir(os.path.join(self.path, name)):
                os.makedirs(os.path.join(self.path, name))
                return "Ok"
            else:
                return "Such directory already exists"
        else:
            return "Wrong input format"

    def delete(self, options):
        if options[0] == "-f":
            name = ' '.join(options[1:])
            if os.path.isfile(os.path.join(self.path, name)):
                os.remove(os.path.join(self.path, name))
                return "Ok"
            else:
                return "Such file does not exist"
        elif options[0] == "-d":
            name = ' '.join(options[1:])
            name.replace("\\", "\\\\")
            if os.path.isdir(os.path.join(self.path, name)):
                try:
                    os.rmdir(os.path.join(self.path, name))
                    return "Ok"
                except OSError:
                    return "Directory is not empty"

            else:
                return "Such directory does not exist"
        else:
            return "Wrong input format"

    def changeDirectory(self, options):
        name = ' '.join(options[1:])
        if name == "..":
            substr = self.path.partition(self.root)[2]
            if substr.count("\\") == 0:
                return "It is a root directory"
            else:
                os.chdir("..")
                self.path = os.getcwd()
                return "Ok"
        else:
            if os.path.isdir(os.path.join(self.path, name)):
                os.chdir(os.path.join(self.path, name))
                self.path = os.getcwd()
                return "Ok"
            else:
                return "Such directory does not exist"


    def open(self, options):
        pass

    def move(self, options):
        pass

    def copy(self, options):
        pass

    def rename(self, options):
        pass

