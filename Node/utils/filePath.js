import { readFileSync } from "fs";

export function getFullPath(currentFilePath, relativePath) {
  let currentFolderTree = currentFilePath.split("/");
  let relativePathTree = relativePath.split("/");
  relativePathTree.forEach((relativePathSegment) => {
    if (relativePathSegment === "..") {
      currentFolderTree.pop();
    } else if (relativePathSegment !== ".") {
      currentFolderTree.push(relativePathSegment);
    }
  });
  let pseudoPath = currentFolderTree.join("/");
  try {
    readFileSync(pseudoPath);
    return pseudoPath;
  } catch (e) {
    try {
      readFileSync(pseudoPath + ".js");
      return pseudoPath + ".js";
    } catch (e) {
      try {
        readFileSync(pseudoPath + "/index.js");
        return pseudoPath + "/index.js";
      } catch (e) {
        try {
          readFileSync(pseudoPath + ".css");
          return pseudoPath + ".css";
        } catch (e) {
          try {
            readFileSync(pseudoPath + ".jsx");
            return pseudoPath + ".jsx";
          } catch (e) {
            return pseudoPath;
          }
        }
      }
    }
  }
}
