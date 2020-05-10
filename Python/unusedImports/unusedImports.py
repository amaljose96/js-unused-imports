
class UnusedImports(object):
    def __init__(self):
        self.filePaths = []
        self.fileQueue = []
        self.packageImports = {}
        self.fileImports = {}
        self.highestDirectory=""
        self.packageStatuses={}
        self.fileStatuses={}
        self.directoryMap={}
        print("Im Ok :)")
        
    def setFilePaths(filePaths):
        self.filePaths=filePaths

# Testing
if __name__ == "__main__":
    web = UnusedImports("")