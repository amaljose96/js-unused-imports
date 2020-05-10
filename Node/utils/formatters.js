import { getFullPath } from "./filePath";

export function formatLocation(currentFilePath,locationSegments){
    let location={};
    let locationString=locationSegments.join(" ");
    let importPath=locationString.split("'").join("").split(";").join("").split("\"").join("");
    if(importPath.includes("/") && importPath.includes(".")){
        location.importType="file";
        let currentFolderPath = currentFilePath.toString().split("/");
        currentFolderPath.pop()
        location.path=getFullPath(currentFolderPath.join("/"),importPath);
    }
    else{
        location.importType="package";
        location.package=importPath;
    }
    return location
}
export function formatVariables(variablesSegments){
    let variablesString = variablesSegments.join(" ");
    let variables=[];
    let includedImports=variablesString.slice(variablesString.indexOf("{"),variablesString.indexOf("}")+1);
    let defaultImport=variablesString.split(includedImports).filter(segment=>segment!=="" && segment!=="{"&& segment!=="}").join("");
    includedImports=includedImports.split("{").join("").split("}").join("").split(" ").join("").split(",")
    defaultImport=defaultImport.split(" ").join("").split(",").join("")
    includedImports.length && includedImports[0]!=="" &&includedImports.forEach((importName)=>{
        variables.push({
            name:importName,
            type:"included"
        });
    });
    if(defaultImport){
        variables.push({
            name:defaultImport,
            type:"default"
        })
    }
    return variables;
}