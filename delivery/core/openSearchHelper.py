from datetime import datetime
import logging
from opensearchpy import OpenSearch


# Helper class for searching OpenSearch
class OpenSearchHelper:
    def __init__(self, host: str, port: int, app_name: str):
        self.host = host
        self.port = port
        self.app_name = app_name

    def transform_to_tid_information(self, data):
        return data.get("tid")

    def transform_to_message_information(self, data):
        return data.get("message") + "\n"

    # Return tids of logs that have a message matching the search text
    def search_tid_by_message(self, search_text: str):
        query = {"match_phrase": {"message": search_text}}
        transform = self.transform_to_tid_information
        return self.search(query, transform)

    # Return only msgs of all logs that have a message matching the sub-string search text
    def search_message_by_partial_message_search(self, search_text: str):
        query = {"match_phrase": {"message": search_text}}
        transform = self.transform_to_message_information
        return self.search(query, transform)

    # Return all messages associated with the given tid
    def search_message_by_tid(self, tid):
        query = {"term": {"tid.keyword": tid}}

        transform = self.transform_to_message_information
        return self.search(query, transform)

    def search(self, query, transform, size_limit=1000):
        client = OpenSearch(
            hosts=[{"host": self.host, "port": self.port}],
            http_compress=True,  # enables gzip compression for request bodies
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            request_timeout=20,
            ssl_show_warn=False,
        )

        search_body = {"size": size_limit, "query": query}
        search_index = f"{self.app_name}-{datetime.utcnow().strftime('%Y.%m.%d')}"

        logging.info(f"Executing search {search_body} on index {search_index}")

        response = client.search(body=search_body, index=search_index)
        data_hits = response.get("hits").get("hits")

        logging.info(f"Found {len(data_hits)} results")

        flat_data_return = [
            transform(current_data.get("_source")) for current_data in data_hits
        ]
        return flat_data_return


# It would need to search 2 times to find the information that we need
# Example how to use this class, for event 'app-web-event'
# open_search_motor = OpenSearchHelper('vpc-c6-dev-es-uw2-logs-dlfqhljpdvbm62vc4qfbsnckji.us-west-2.es.amazonaws.com',443,'app-web-event')
# data = open_search_motor.search_message_by_tid("[tx:NUCS03US7O8UPCRKSNKHHH4V2G pl:[62PKC8MDTP029CQ64B6UT414NO]]")


# Example how to use this class, for delivery 'app-web-event'
# open_search_motor = OpenSearchHelper("vpc-c6-dev-es-uw2-logs-dlfqhljpdvbm62vc4qfbsnckji.us-west-2.es.amazonaws.com",443,"app-web-delivery",)
# data = open_search_motor.search_message_by_tid("[tx:T6PKQCUS9G8UPCRKSNKHHH4V2G pl:62PKC8MDTP029CQ64B6UT414NO]")
