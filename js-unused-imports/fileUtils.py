import json
def writeJsonToFile(obj,fileName):
    outputFile = open(fileName, "w")
    outputFile.write(json.dumps(obj, sort_keys=True,
                                indent=4, separators=(',', ': ')))