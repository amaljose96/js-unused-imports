
def getFullPath(currentFilePath, relativePath):
    fullFolderTree = currentFilePath.split("/")[0:-1]
    relativePathTree = relativePath.split("/")
    for folder in relativePathTree:
        if(folder == "."):
            continue
        elif(folder == ".."):
            fullFolderTree = fullFolderTree[0:-1]
        else:
            fullFolderTree.append(folder)
    return "/".join(fullFolderTree)


def getCorrectFilePath(filePath):
    tryPath = filePath
    try:
        tryFile = open(tryPath)
        return tryPath
    except:
        tryPath = filePath+".js"
        try:
            tryFile = open(tryPath)
            return tryPath
        except:
            tryPath = filePath+".jsx"
            try:
                tryFile = open(tryPath)
                return tryPath
            except:
                tryPath = filePath+"index.js"
                try:
                    tryFile = open(tryPath)
                    return tryPath
                except:
                    tryPath = filePath+"/index.js"
                    try:
                        tryFile = open(tryPath)
                        return tryPath
                    except:
                        tryPath = filePath+"/index.jsx"
                        try:
                            tryFile = open(tryPath)
                            return tryPath
                        except:
                            return ""

def getHighestDirectory(filesList):
    highestDirectory = filesList[0].split("/")
    for filePath in filesList:
        fileDirectory = filePath.split("/")
        commonDirectory = []
        for segment in fileDirectory:
            if segment in highestDirectory:
                commonDirectory.append(segment)
            else:
                break
        highestDirectory = commonDirectory
    highestDirectory = "/".join(highestDirectory)+"/"
    return highestDirectory
