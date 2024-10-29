from authorizationContext import AuthorizationContext
from configuration import Configuration


class Context:
    def __init__(
        self,
        case_name: str,
        folder_to_write: str,
        override_options: dict,
        configuration=Configuration()
    ):
        self.authorization_context = AuthorizationContext(configuration)
        self.configuration = configuration
        self.case_name = case_name
        self.folder_to_write = folder_to_write
        self.override_options = override_options
