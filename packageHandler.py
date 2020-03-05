import fileUtils
import json
def handleUsed(packageImports):
    print("\nUsed packages:")
    for package in sorted(packageImports.keys()):
        print("\t"+package)
    fileUtils.writeJsonToFile(packageImports,"packageImports.json")

def getPackageJsonContent(highestDirectory):
    print("\nScanning current package list\n")
    packageFile = None
    packageDirectory = highestDirectory[0:-1]
    while packageFile == None and packageDirectory != "":
        try:
            print("Searching for package.json at " +
                packageDirectory+"/package.json")
            packageFile = open(packageDirectory+"/package.json")
            print("\nFound package.json at "+packageDirectory+"/package.json")
        except:
            print("Did not find package.json in "+packageDirectory)
            packageDirectory = "/".join(packageDirectory.split("/")[0:-1])
    packageFileContent = packageFile.read()
    packageJson = json.loads(packageFileContent)
    return packageJson

def getPackageStatuses(packageJson,packageImports):
    packageStatuses={}
    for packageDependency in sorted(packageJson["dependencies"].keys()):
        packageType = ""
        if(packageDependency in packageImports.keys()):
            packageStatuses[packageDependency] = True
        else:
            packageStatuses[packageDependency] = False
    return packageStatuses

def printPackageStatuses(packageStatuses):
    print("\nCurrent package dependecies :")
    for package in sorted(packageStatuses.keys()):
        if(packageStatuses[package]):
            print("\t\33[32mUSED    | "+package+"\033[0m")
        else:
            print("\t\033[91mUNUSED | "+package+"\033[0m")

def printUnusedCount(packageStatuses):
    unusedPackageCount = 0
    for packageStatus in packageStatuses.values():
        unusedPackageCount = unusedPackageCount+packageStatus
    print("Unused packages : "+str(unusedPackageCount) +
        " out of "+str(len(packageStatuses.keys())) + " | "+str((unusedPackageCount*100.00)/len(packageStatuses.keys()))+"%")
    

