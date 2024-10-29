from authorizationContext import AuthorizationContext
from configuration import Configuration


class Context:
    def __init__(self, override_options={}):
        self.configuration = Configuration()
        self.authorization_context = AuthorizationContext(self.configuration)
        self.override_options = override_options
