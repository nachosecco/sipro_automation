from pathlib import Path
import os


class TemplateGeneratorShellScriptForReadLog:
    def __init__(self, id: str):
        self.id = id

    def generateDelivery(self):
        hostToRead = os.getenv(
            "READ_LOG_HOST_TO_CONNECT_DELIVERY",
            "CHANGE_ENV_VAR_READ_LOG_HOST_TO_CONNECT_DELIVERY",
        )
        pathToLog = os.getenv(
            "READ_LOG_PATH_DELIVERY", "CHANGE_ENV_VAR_READ_LOG_PATH_DELIVERY"
        )
        return self.__generate("script_delivery_read_log.sh", hostToRead, pathToLog)

    def generateEvents(self):
        hostToRead = os.getenv(
            "READ_LOG_HOST_TO_CONNECT_EVENTS",
            "CHANGE_ENV_VAR_READ_LOG_HOST_TO_CONNECT_EVENTS",
        )
        pathToLog = os.getenv(
            "READ_LOG_PATH_EVENTS", "CHANGE_ENV_VAR_READ_LOG_PATH_EVENTS"
        )
        return self.__generate("script_events_read_log.sh", hostToRead, pathToLog)

    def __generate(self, shellFileToCreate, hostToRead, pathToLog):
        directoryPath = "build/case" + self.id + "/"
        os.makedirs(directoryPath, exist_ok=True)

        fileShell = Path(directoryPath + shellFileToCreate)
        if not (fileShell.exists()):
            sshCommand = os.getenv("READ_LOG_SSH_COMMAND", "ssh")
            sshUser = os.getenv("READ_LOG_USER_SSH", "jenkins")
            logLines = os.getenv("READ_LOG_LINES_TO_READ", "8000")

            with open("resources/script_template_read_log.sh", "r") as template:
                scriptTemplate = template.read()
                print(sshUser)
                scriptTemplate = scriptTemplate.replace(
                    "${READ_LOG_SSH_COMMAND}", sshCommand
                )
                scriptTemplate = scriptTemplate.replace("${READ_LOG_USER}", sshUser)
                scriptTemplate = scriptTemplate.replace(
                    "${READ_LOG_HOST_TO_CONNECT}", hostToRead
                )
                scriptTemplate = scriptTemplate.replace("${READ_LOG_PATH}", pathToLog)
                scriptTemplate = scriptTemplate.replace(
                    "${READ_LOG_LINES_TO_READ}", logLines
                )

                with open(fileShell, "w+") as writefile:
                    writefile.write(scriptTemplate)

        return os.path.abspath(fileShell)


# This would create a file in html using the template of html that has the library in js for vast parsing
class TemplateGeneratorVastClientParser:
    def __init__(self, id: str):
        self.id = id

    def generate(self, vastXML: str) -> str:
        directoryPath = "build/case" + self.id + "/"
        os.makedirs(directoryPath, exist_ok=True)

        with open("resources/vast_parse_template.html", "r") as template:
            htmlTemplate = template.read()
            resultToWrite = htmlTemplate.replace("${REPLACE_VAST}", vastXML)
            with open(directoryPath + "vast_parse_client.html", "w+") as writefile:
                writefile.write(resultToWrite)
        return os.path.abspath(directoryPath + "vast_parse_client.html")
