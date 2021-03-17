import os

class WinMng:

    def __init__(self, path):
        """Constructor"""
        self.path = path

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

    def open(self, options):
        pass

    def mov(self, options):
        pass

    def cop(self, options):
        pass

    def renam(self, options):
        pass