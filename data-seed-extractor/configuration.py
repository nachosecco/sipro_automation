import os


class Configuration:
    """Class that is has all external(env) configurations already loaded"""

    def __init__(self):
        self.environment = os.getenv("DSE_ENVIRONMENT")
        self.dashboard_api = os.getenv("DSE_DASHBOARD_API")
        self.api_user = os.getenv("DSE_API_USER")
        self.api_pwd = os.getenv("DSE_API_PWD")
        self.inventory_router_api = os.getenv("DSE_INVENTORY_ROUTER_API")
        self.media_server_url = os.getenv("DSE_MEDIA_SERVER_URL")
