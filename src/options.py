
import os


class Options:
    debug = False
    optimize = False
    optimizeLevel = 0
    printAssembly = False
    printIR = False

    # Filepaths
    filepath = None
    rootpath = None
    filename = None
    filenameNoExt = None
    objectFilepath = None
    executableFilepath = None

    def setFilepath(self, filepath):
        self.filepath = filepath
        self.rootpath = os.path.dirname(filepath)
        self.filename = os.path.basename(filepath)
        self.filenameNoExt = os.path.splitext(self.filename)[0]
        self.objectFilepath = os.path.join(self.rootpath, self.filenameNoExt + ".o")
        self.executableFilepath = os.path.join(self.rootpath, self.filenameNoExt)
        if os.name == "nt":
            # Add .exe extension on Windows
            self.executableFilepath += ".exe"
