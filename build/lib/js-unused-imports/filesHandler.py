import fileUtils
import scanner
def getUsedDirectoryTree(fileImports,highestDirectory):
    usedFilesList=list(fileImports.keys())
    usedDirectoryMap = {}
    for filePath in usedFilesList:
        relativeFilePath = filePath.split(highestDirectory)[1]
        traversedPath = []
        for segment in relativeFilePath.split("/"):
            currentTree = usedDirectoryMap
            for path in traversedPath:
                currentTree = currentTree[path]
            if segment == relativeFilePath.split("/")[-1]:
                currentTree[segment] = fileImports[filePath]
            elif segment not in currentTree:
                currentTree[segment] = {}
            traversedPath.append(segment)
    usedDirectoryMap = {
        highestDirectory: usedDirectoryMap
    }
    return usedDirectoryMap


def printTree(node, level):
    if(type(node) is list):
        return
    if(type(node) is bool):
        return
    subTreeNames = sorted(list(node.keys()))
    for subFolder in subTreeNames:
        printArray = []
        for i in range(0, level+1):
            printArray.append("")
        indentationString = "\t".join(printArray)
        printText = indentationString+"|-"+subFolder
        if(type(node[subFolder]) is bool):
            if(node[subFolder]):
                print("\33[32m"+printText+"\033[0m")
            else:
                print("\033[91m"+printText+"\033[0m")
        else:
            print(printText)
        printTree(node[subFolder], level+1)

def handleUsed(usedDirectoryMap):
    print("\nUsed Files Directory Structure : \n")
    printTree(usedDirectoryMap, 0)
    fileUtils.writeJsonToFile(usedDirectoryMap,"fileImports.json")

def getFileStatuses(highestDirectory,fileImports):
    fileStatuses=[]
    print("\nScanning File Structure\n")
    print("Scanning "+highestDirectory)
    filesList = scanner.getFilesList(highestDirectory)
    for fileName in filesList:
        fileType = ""
        if(fileName in list(fileImports.keys())):
            fileStatuses.append({"fileName": fileName, "used": True})
        else:
            fileStatuses.append({"fileName": fileName, "used": False})
    return fileStatuses

def getDirectoryTree(fileStatuses,highestDirectory):
    directoryMap = {}
    for fileStatus in fileStatuses:
        filePath = fileStatus["fileName"]
        relativeFilePath = filePath.split(highestDirectory)[1]
        traversedPath = []
        for segment in relativeFilePath.split("/"):
            currentTree = directoryMap
            for path in traversedPath:
                currentTree = currentTree[path]
            if segment == relativeFilePath.split("/")[-1]:
                currentTree[segment] = fileStatus["used"]
            elif segment not in currentTree:
                currentTree[segment] = {}
            traversedPath.append(segment)
    return directoryMap

def printFileStatuses(directoryMap):
    printTree(directoryMap, 0)

def printUnusedCount(fileStatuses):
    unusedFilesCount = 0
    for fileStatus in fileStatuses:
        unusedFilesCount = unusedFilesCount+fileStatus["used"]
    print("Unused files : "+str(unusedFilesCount) +
        " out of "+str(len(fileStatuses)) + " | "+str((unusedFilesCount*100.00)/len(fileStatuses))+"%")