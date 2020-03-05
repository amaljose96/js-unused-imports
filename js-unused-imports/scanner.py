import sys
import os
import filePathUtils
def scanDependencies(fileQueue,packageImports,fileImports):
    while len(fileQueue) != 0:
        currentFile = fileQueue[0]
        try:
            f = open(currentFile)
            for line in f:
                importDirectory=""
                if ("import" in line and len(line.split("from")) > 1):
                    importDirectory = line.rstrip("\n").split("from")[1].replace(
                        "\"", "").replace(" ", "").replace(";", "").replace("'", "").replace("\t", "")
                elif("require(" in line):
                    importDirectory = line.split("require(")[1].split(")")[0].replace(
                        "\"", "").replace(" ", "").replace(";", "").replace("'", "").replace("\t", "")
                else:
                    continue
                if len(importDirectory.split("/")) == 1 or len(importDirectory.split("@")) != 1 or importDirectory.find("lodash") != -1:
                    if(importDirectory not in packageImports):
                        packageImports[importDirectory] = [currentFile]
                    else:
                        packageImports[importDirectory].append(currentFile)
                    continue
                else:
                    fullPath = filePathUtils.getFullPath(currentFile, importDirectory)
                    correctPath = filePathUtils.getCorrectFilePath(fullPath)
                    if correctPath == "":
                        print("\nFile "+fullPath+" missing !!\nFile was imported in " +
                                currentFile+" as "+importDirectory)
                        continue
                    if correctPath in list(fileImports.keys()):
                        fileImports[correctPath].append(currentFile)
                    else:
                        fileImports[correctPath] = [currentFile]
                        fileQueue.append(correctPath)
        except:
            print("Failed to open "+currentFile)
        fileQueue = fileQueue[1:]

def getFilesList(directory):
    filesList=[]
    for path in os.walk(directory):
        pathName = path[0]
        currentFolders = path[1]
        currentFiles = path[2]
        for fileName in currentFiles:
            if(".js" in fileName or ".jsx" in fileName):
                filesList.append(pathName+"/"+fileName)
    return filesList