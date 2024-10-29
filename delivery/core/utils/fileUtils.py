import os


def findfiles(name: str, ext: str, path=""):
    if not path:
        path = os.getenv("AUTOMATION_PATH", "CHANGE_AUTOMATION_PATH")
        if path == "CHANGE_AUTOMATION_PATH":
            raise Exception("The variable AUTOMATION_PATH is required")
    foundFiles = []
    for dirpath, dirname, files in os.walk(path):
        for file in files:
            if file.startswith(name) and file.endswith(ext):
                foundFiles.append(os.path.join(dirpath, file))
    return foundFiles
