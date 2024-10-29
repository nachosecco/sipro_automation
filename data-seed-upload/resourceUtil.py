import logging

import requests

from context import Context

# These are general keys, that we don't want to take from the original data
DEFAULT_KEYS_TO_SANITIZE = ["id", "auditEvent", "createdAt", "updatedAt", "guid"]


def sanitize(resource, keys_to_sanitize):
    """It will remove the keys that should not be in a resource to create/update"""
    data = resource.copy()
    keys_to_sanitize = keys_to_sanitize + DEFAULT_KEYS_TO_SANITIZE
    for key in keys_to_sanitize:
        data.pop(key, None)

    return data


class ResourceUtil:
    def __init__(self, context: type(Context)):
        self.logger = logging.getLogger("upload")
        self.headers = self.__get_headers(context)

    def __get_headers(self, context):
        headers = {"Authorization": context.authorization_context.token}

        if "company_id" in context.override_options:
            headers["X-COMPANY-OVERRIDE"] = str(context.override_options["company_id"])

        return headers

    def load_index(self, url, resource_name_log):
        """Load resources index(collections)"""
        if url.endswith("/"):
            url = url[:-1]  # Remove the last / if it exists

        if url.endswith("/."):
            url = url[:-2]

        log_message = f"{resource_name_log} by id index"

        return self.__get_resource_by_url(url, log_message)

    def get_resource_by_id(self, url: str, resource_id: int, resource_name_log: str):
        """Will get a resource by id and return the json dict"""
        log_message = f"{resource_name_log} by id {resource_id}"
        return self.__get_resource_by_url(url, log_message)

    def __get_resource_by_url(self, url: str, resource_name_message: str):
        """Generic get that will return a json"""
        self.logger.debug(f"Fetching {resource_name_message}")

        response = requests.request(
            method="GET",
            url=url,
            headers=self.headers,
        )
        if not (response.status_code == 200):
            raise Exception(
                f"error fetching {resource_name_message} have the status code {response.status_code} "
                f"and message {response.text}"
            )
        return response.json()

    def sync(
        self,
        url,
        resource_data,
        resource_by_name,
        resource_default_values,
        resource_name_log,
        name_key="name",
    ):
        """It will try to create/update a resource by using the resource name_key"""
        resource_name = resource_data.get(name_key)
        self.logger.info(f"Sync {resource_name_log} with {name_key} {resource_name}")

        request_body = resource_default_values.copy()
        request_body.update(resource_data)

        found_resource = resource_by_name.get(resource_name, None)

        if found_resource is None:
            self.logger.debug(
                f"Not found {resource_name_log} we are going to create one"
            )

            data, name = self.create_update_delete_resource(
                request_body, resource_name_log, url, "POST", name_key
            )
            id_resource = data.get("id")

            self.logger.info(
                f"Created {resource_name_log} of the {name_key} {name} with id {id_resource}"
            )

            return data
        else:
            id_resource = found_resource.get("id")
            current_name = found_resource.get(name_key)
            self.logger.debug(
                f"Found {resource_name_log} with id {id_resource} and {name_key}[{current_name}] we are updating"
            )
            url = f"{url}/{id_resource}"
            request_body["id"] = id_resource
            data, name = self.create_update_delete_resource(
                request_body, resource_name_log, url, "PUT"
            )

            self.logger.info(
                f"Updated {resource_name_log} of the {name_key} {name} with id {id_resource}"
            )
            return data

    def upload_file(self, file_body, form_body, url, resource_name_log):
        """Method to upload a file with a form body"""
        self.logger.info(f"Upload file to {resource_name_log}")
        response = requests.request(
            method="POST",
            url=url,
            files=file_body,
            params=form_body,
            headers=self.headers,
        )
        if not (response.status_code == 201 or response.status_code == 200):
            self.logger.error(
                f"there was error uploading file to {resource_name_log} the error message is {response.text}"
            )
            raise Exception(
                f"error creating {resource_name_log} have the status code {response.status_code} "
                f"and message {response.text}"
            )
        data = response.json()
        return data

    def create_update_delete_resource(
        self, request_body, resource_name_log, url, method, key_name="name"
    ):
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=request_body,
        )
        if not (
            response.status_code == 201
            or response.status_code == 200
            or response.status_code == 204
        ):
            self.logger.error(
                f"there was error with method {method} {resource_name_log} the "
                f"object with key/values of {request_body} and the error message {response.text}"
            )
            raise Exception(
                f"error creating {resource_name_log} have the status code {response.status_code} "
                f"and message {response.text}"
            )
        data = response.json()
        name = data.get(key_name)
        return data, name
