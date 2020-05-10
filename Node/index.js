import { getFullPath } from "./utils/filePath";
import config from "./config.json";
import { readFileSync } from "fs";
import { formatLocation, formatVariables } from "./utils/formatters";
import { uniquePush } from "./utils/utils";

let filesData = {};

console.log("Running Unused Imports Finder. v0.0.1");
console.log("Running from " + process.cwd());

function prepareLaunchSequence() {
  config.projects.forEach((project) => {
    filesData[project.name] = { files: {} };
    project.files.forEach((filePath) => {
      let fullPath = getFullPath(process.cwd(), filePath);
      filesData[project.name].files[fullPath] = {};
      filesData[project.name].structure = placeFileInStructure(
        filesData[project.name].structure,
        fullPath
      );
      filesData[project.name].fileQueue = [fullPath];
    });
  });
}

function placeFileInStructure(structure = {}, filePath = "", level = 0) {
  let segments = filePath.split("/");
  let currentSegment = segments[level];
  if (level === segments.length) {
    return currentSegment;
  }
  return {
    ...structure,
    [currentSegment]: placeFileInStructure(
      structure[currentSegment],
      filePath,
      level + 1
    ),
  };
}
function getFileProperties(filePath) {
  //This would list the exported functions/variables, imported functions/variables in this file.
  //Also this places the file in the folder tree.
  let fileProperties = {
    dependentFiles: [],
    dependentPackages: [],
    imports: [],
    exports: [],
  };
  const data = readFileSync(filePath, "utf8");
  let lines = data.split("\n");
  lines.forEach((line, index) => {
    let tokens = line.split(" ");
    if (tokens[0] === "import") {
      tokens = tokens.slice(1);
      if (tokens.includes("from")) {
        let location = formatLocation(
          filePath,
          tokens.slice(tokens.indexOf("from") + 1)
        );
        let variables = formatVariables(
          tokens.slice(0, tokens.indexOf("from"))
        );
        if (location.importType === "file") {
          fileProperties.dependentFiles.push(location.path);
        } else {
          fileProperties.dependentPackages.push(location.package);
        }
        variables.forEach((variable) => {
          fileProperties.imports.push({
            ...location,
            name: variable.name,
            type: variable.type,
          });
        });
      } else if (tokens[0] === "{") {
        let nextFewLines = [];
        let cursor = index + 1;
        while (lines[cursor].split(" ").join("")[0] !== "}" && lines[cursor]) {
          nextFewLines.push(lines[cursor]);
          cursor = cursor + 1;
        }
        tokens = lines[cursor].split(" ");
        let location = formatLocation(
          filePath,
          tokens.slice(tokens.indexOf("from") + 1)
        );

        let variables = formatVariables(["{", ...nextFewLines, "}"]).filter(
          (variable) => variable.name !== ""
        );

        if (location.importType === "file") {
          fileProperties.dependentFiles.push(location.path);
        } else {
          fileProperties.dependentPackages.push(location.package);
        }
        variables.forEach((variable) => {
          fileProperties.imports = uniquePush(fileProperties.imports, {
            ...location,
            name: variable.name,
            type: variable.type,
          });
        });
      } else {
        console.log("Un handled import ", tokens, " in ", filePath);
      }
    } else if (tokens[0] === "export") {
      if (tokens[1] === "default") {
        let exportName = tokens[2].split(";").join("").split("=")[0];
        if (exportName !== "{") {
          fileProperties.exports = uniquePush(fileProperties.exports, {
            name: tokens[2].split(";").join("").split("=")[0],
            type: "default",
            usage: 0,
          });
        } else {
          let nextFewLines = [];
          let cursor = index + 1;
          let bracketCount = 0;
          while (bracketCount >= 0 && lines[cursor]) {
            if (bracketCount == 0 && !lines[cursor].includes("}")) {
              nextFewLines.push(lines[cursor].split(":")[0].split("(")[0]);
            }
            if (lines[cursor].includes("{")) {
              bracketCount = bracketCount + 1;
            } else if (lines[cursor].includes("}")) {
              bracketCount = bracketCount - 1;
            }
            cursor = cursor + 1;
          }
          nextFewLines.forEach((exportLine) => {
            fileProperties.exports = uniquePush(fileProperties.exports, {
              name: exportLine
                .split(" ")
                .join("")
                .split("\t")
                .join("")
                .split(";")
                .join("")
                .split("=")[0],
              type: "included",
              usage: 0,
            });
          });
        }
      } else if (tokens[1] === "const") {
        fileProperties.exports = uniquePush(fileProperties.exports, {
          name: tokens[2].split(";").join("").split("=")[0],
          type: "included",
          usage: 0,
        });
      } else if (tokens[1] === "function") {
        fileProperties.exports = uniquePush(fileProperties.exports, {
          name: tokens[2].split("(")[0],
          type: "included",
          usage: 0,
        });
      } else {
        console.log("Un handled ", tokens);
      }
    }
  });
  return fileProperties;
}

prepareLaunchSequence();
Object.keys(filesData).forEach((project) => {
  console.log("Project : ", project);
  let projectData = filesData[project];
  let levels = 0;
  while (projectData.fileQueue.length !== 0) {
    let file = projectData.fileQueue[0];
    projectData.files[file] = getFileProperties(file);
    projectData.structure = placeFileInStructure(
      filesData[project].structure,
      file
    );
    projectData.files[file].dependentFiles.forEach((newFile) => {
      if (!Object.keys(projectData.files).includes(newFile)) {
        projectData.fileQueue.push(newFile);
      }
    });
    projectData.fileQueue = projectData.fileQueue.slice(1);
    levels = levels + 1;
  }
  delete projectData.fileQueue;
  console.log("Processed", levels, "files");
  projectData.packages = {};
  Object.keys(projectData.files).forEach((file) => {
    projectData.files[file].imports.forEach((importedVariable) => {
      if (importedVariable.importType === "package") {
        let variableKey = importedVariable.package;
        if (!projectData.packages[variableKey]) {
          projectData.packages[variableKey] = 1;
        } else {
          projectData.packages[variableKey] =
            projectData.packages[variableKey] + 1;
        }
      } else {
        let importedFileData = projectData.files[importedVariable.path];
        importedFileData.exports = importedFileData.exports.map(
          (exportedVariable) => {
            if (
              (importedVariable.type === "default" &&
                exportedVariable.type === "default") ||
              (importedVariable.type === "included" &&
                exportedVariable.name === importedVariable.name)
            ) {
              return {
                ...exportedVariable,
                usage: exportedVariable.usage + 1,
              };
            }
            return exportedVariable;
          }
        );
      }
    });
  });
});
console.log(JSON.stringify(filesData, null, 4));
