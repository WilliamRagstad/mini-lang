
import os


class Options:
    debug = False
    filepath = None
    rootpath = None
    filename = None

    def setFilepath(self, filepath):
        self.filepath = filepath
        self.rootpath = os.path.dirname(filepath)
        self.filename = os.path.basename(filepath)
