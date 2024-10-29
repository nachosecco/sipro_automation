import logging
import os.path

from context import Context
from customFormatter import CustomFormatter
from dashboardApiEnvironmentResources import DashboardApiEnvironmentResources
from reader import Reader


class UploaderReader:
    def __init__(
        self,
    ):
        self.__setup_logger()
        self.company_cache = self.__get_company_cache()

    def __setup_logger(self):
        logger = logging.getLogger("upload")
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        ch.setFormatter(CustomFormatter())

        logger.addHandler(ch)

        self.logger = logger

    def __get_company_cache(self):
        return DashboardApiEnvironmentResources().load_companies(Context())

    def upload_file(self, path_to_file: str):
        directory_case = os.path.dirname(path_to_file)
        reader = Reader(path_to_file).read()

        context = Context(override_options=reader.get("override_options", {}))

        if "company_name" in context.override_options:
            company_name = context.override_options["company_name"]
            if company_name in self.company_cache:
                context.override_options["company_id"] = self.company_cache[
                    company_name
                ]["id"]
            else:
                raise RuntimeError(
                    f"No Company ID found for Override Company Name: {company_name}"
                )

        return self.upload(
            reader,
            context,
            directory_case,
        )

    def upload(
        self,
        reader,
        context,
        directory_case,
    ):
        pass
