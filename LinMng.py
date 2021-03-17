class LinMng:

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

    def delete(self, options):
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

    def open(self, options):
        pass

    def move(self, options):
        pass

    def copy(self, options):
        pass

    def rename(self, options):
        pass

    def changeDirectory(self, options):
        name = ' '.join(options)
        if name == "..":
            substr = self.path.partition(self.root)[2]
            if substr.count("\\") == 0:
                return "It is a root directory"
            else:
                os.system('cd ..')
                self.path = os.getcwd()
                return "Ok"
        else:
            if not (self.root in name):
                name = os.path.join(self.path, name)
            if os.path.isdir(name):
                os.system('cd ' + name)
                self.path = os.getcwd()
                self.print_content()
                return "Ok"
            else:
                return "Such directory does not exist"

    def print_content(self):
        for i in os.listdir(self.path):
            print(i)