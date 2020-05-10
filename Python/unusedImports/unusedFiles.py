
import sequences


filePaths = [
                "../../../UnifiedDashboard/apps/ui/src/index.js",
                ]
fileQueue = []
packageImports = {}
fileImports = {}
highestDirectory=""
packageStatuses={}
fileStatuses={}
directoryMap={}

sequences.printHeader()
sequences.prepareFileQueue(filePaths,fileQueue)
sequences.scanFiles(fileQueue,packageImports,fileImports)
highestDirectory=sequences.gettingProjectDirectory(fileImports)
sequences.displayUsedPackages(packageImports)
sequences.displayUsedFiles(fileImports,highestDirectory)
packageStatuses=sequences.displayAllPackages(packageImports,highestDirectory)
fileStatuses=sequences.displayAllFiles(fileImports,highestDirectory,directoryMap)
sequences.printUnusedPackagesCount(packageStatuses)
sequences.printUnusedFilesCount(fileStatuses)
sequences.generateUnusedPackagesJson(packageStatuses)
sequences.generateUnusedFilesJson(directoryMap)
