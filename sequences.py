import os
import sys
import json
import scanner
import filePathUtils
import fileUtils
import packageHandler
import filesHandler

def printHeader():
    print("\nUnused Files Detector.")
    print("======================")
    print("Author : Amal Jose\n\n")

def prepareFileQueue(filePaths,fileQueue):
    cwd = os.getcwd()+"/."
    for filePath in filePaths:
        fileQueue.append(filePathUtils.getFullPath(cwd,filePath))

def scanFiles(fileQueue,packageImports,fileImports):
    print("Scanning dependencies...")
    scanner.scanDependencies(fileQueue,packageImports,fileImports)
    if(len(fileImports.keys()) == 0):
        print("No Files Found")
        exit()
    print("\nProject Scan Complete")
    print("\n=========================================")

def gettingProjectDirectory(fileImports):
    highestDirectory = filePathUtils.getHighestDirectory(fileImports.keys())
    print("\nProject Directory : "+highestDirectory+"\n")
    return highestDirectory

def displayUsedPackages(packageImports):
    packageHandler.handleUsed(packageImports)

def displayUsedFiles(fileImports,highestDirectory):
    usedDirectoryMap = filesHandler.getUsedDirectoryTree(fileImports,highestDirectory)
    filesHandler.handleUsed(usedDirectoryMap)

def displayAllPackages(packageImports,highestDirectory):
    packageJson = packageHandler.getPackageJsonContent(highestDirectory)
    packageStatuses = packageHandler.getPackageStatuses(packageJson,packageImports)
    packageHandler.printPackageStatuses(packageStatuses)
    return packageStatuses

def displayAllFiles(fileImports,highestDirectory,directoryMap):
    fileStatuses = filesHandler.getFileStatuses(highestDirectory,fileImports)
    directoryMapCopy=filesHandler.getDirectoryTree(fileStatuses,highestDirectory)
    for key in directoryMapCopy.keys():
        directoryMap[key]=directoryMapCopy[key]
    filesHandler.printFileStatuses(directoryMap)
    return fileStatuses

def printUnusedPackagesCount(packageStatuses):
    packageHandler.printUnusedCount(packageStatuses)

def printUnusedFilesCount(fileStatuses):
    filesHandler.printUnusedCount(fileStatuses)

def generateUnusedPackagesJson(packageStatuses):
    print("\nGenerating unusedPackages.json")
    fileUtils.writeJsonToFile(packageStatuses,"unusedPackages.json")
    print("File Generated.")

def generateUnusedFilesJson(directoryMap):
    print("\nGenerating unusedFiles.json")
    fileUtils.writeJsonToFile(directoryMap,"unusedFiles.json")
    print("File Generated.")
